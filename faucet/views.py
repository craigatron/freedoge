import logging
import os

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.generic import View
from jsonrpclib import Server

DOGE_AMOUNT = 0.01


class FreeDoge(View):
  def get(self, request, *args, **kwargs):
    return render(request, 'base.html',
        dictionary={'faucet_addr': os.environ['FAUCET_ADDR']},
        context_instance=RequestContext(request))

  def post(self, request, *args, **kwargs):
    dictionary={'faucet_addr': os.environ['FAUCET_ADDR']}
    try:
      server = get_rpc_server()
      send_addr = request.POST.get('addr', '')
      is_valid_resp = server.validateaddress(send_addr)
      is_valid = is_valid_resp['isvalid']
      if is_valid:
        dictionary['send_addr'] = send_addr
        remaining_balance = server.getbalance()
        if remaining_balance and remaining_balance > DOGE_AMOUNT:
          send_resp = server.sendtoaddress(send_addr, DOGE_AMOUNT)
          if 'code' in send_resp:
            dictionary['error'] = send_resp['message']
          else:
            dictionary['transaction'] = send_resp
      else:
        dictionary['error'] = 'invalid address!'
    except Exception as e:
      logging.error('error: ' + str(e))
      dictionary['error'] = 'couldn\'t connect to dogecoin! :('
    return render(request, 'base.html', dictionary,
        context_instance=RequestContext(request))


def get_rpc_server():
  url = 'http://%s:%s@%s' % (os.environ['DOGEUSER'],
                             os.environ['DOGEPASS'],
                             os.environ['DOGESERVER'])
  return Server(url)
