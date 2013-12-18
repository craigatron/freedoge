from datetime import datetime, timedelta
import logging
import os

from django.core.exceptions import ValidationError
from django.core.validators import validate_ipv4_address
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.utils.timezone import utc
from django.views.generic import View
from faucet import dogecoin_client
from faucet.models import Transaction
from ratelimit.decorators import ratelimit
from recaptcha.client import captcha

DOGE_ACCOUNT = os.environ['DOGE_ACCOUNT']
DOGE_AMOUNT = float(os.environ['DOGE_AMOUNT'])

@ratelimit(block=True, method='POST')
def freedoge(request):
  if request.method == 'GET':
    dictionary = {}
    try:
      if not should_give_doge(request):
        dictionary['error'] = 'naughty shibe already got doge, can get more doge in 1 week'
        dictionary['hide_input'] = True
    except ValidationError as e:
      logging.warning(str(e))
      dictionary['error'] = 'naughty shibe, that\'s not a real IP address'
    return render(request, 'base.html', dictionary,
                  context_instance=RequestContext(request))

  elif request.method == 'POST':
    send_addr = request.POST.get('addr', '')
    captcha_response = captcha.submit(
        request.POST.get('recaptcha_challenge_field'),
        request.POST.get('recaptcha_response_field'),
        os.environ['CAPTCHA_SECRET_KEY'],
        request.META['REMOTE_ADDR'])
    if not captcha_response.is_valid:
      return render(request, 'base.html',
          {'error':   'bad captcha!'},
          context_instance=RequestContext(request))
    try:
      if not should_give_doge(request, send_addr):
        return render(request, 'base.html',
            {'error': 'naughty shibe already got doge, can get more doge in 1 week',
             'hide_input': True},
            context_instance=RequestContext(request))
    except ValidationError as e:
      return render(request, 'base.html',
          {'error': 'naughty shibe, that\'s not a real IP address'},
          context_instance=RequestContext(request))

    dictionary = {}
    try:
      server = dogecoin_client.get_rpc_server()
      is_valid_resp = server.validateaddress(send_addr)
      is_valid = is_valid_resp['isvalid']
      if is_valid:
        dictionary['send_addr'] = send_addr
        remaining_balance = server.getbalance(DOGE_ACCOUNT)
        if remaining_balance and remaining_balance > DOGE_AMOUNT:
          tx = Transaction(ip_address=get_ip(request),
                           sent_address=send_addr,
                           tx_time=datetime.utcnow().replace(tzinfo=utc))
          send_resp = server.sendfrom(DOGE_ACCOUNT, send_addr, DOGE_AMOUNT)
          if 'code' in send_resp:
            dictionary['error'] = send_resp['message']
          else:
            tx.save()
            dictionary['transaction'] = send_resp
        else:
          dictionary['error'] = 'not enough doge left to send :('
      else:
        dictionary['error'] = 'invalid address!'
    except Exception as e:
      logging.error('error: ' + str(e))
      dictionary['error'] = 'couldn\'t connect to dogecoin! :('
    return render(request, 'base.html', dictionary,
        context_instance=RequestContext(request))


def get_ip(request):
  x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
  if x_forwarded_for:
    logging.info('xforwadedfor: %s', x_forwarded_for)
    ip = x_forwarded_for.split(',')[-1]
  else:
    ip = request.META.get('REMOTE_ADDR')
  return ip


def should_give_doge(request, send_addr=None):
  ip = get_ip(request)
  validate_ipv4_address(ip)
  week_ago = datetime.utcnow().replace(tzinfo=utc) - timedelta(days=7)
  query = Q(ip_address=ip)
  if send_addr:
    query = query | Q(sent_address=send_addr)
  transactions = Transaction.objects.filter(query).filter(tx_time__gt=week_ago)
  return len(transactions) == 0
