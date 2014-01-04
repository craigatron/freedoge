import logging
import os

from django.conf import settings
from faucet import dogecoin_client

DOGE_AMOUNT = float(os.environ['DOGE_AMOUNT'])

def template_constants(request):
  faucet_address = os.environ['FAUCET_ADDR']
  dictionary = {'FAUCET_ADDR': faucet_address}
  if settings.ANALYTICS_ID:
    dictionary['ANALYTICS_ID'] = settings.ANALYTICS_ID

  if 'ADSENSE_CLIENT' in os.environ and 'ADSENSE_SLOT' in os.environ:
    dictionary['ADSENSE_CLIENT'] = os.environ['ADSENSE_CLIENT']
    dictionary['ADSENSE_SLOT'] = os.environ['ADSENSE_SLOT']

  try:
    server = dogecoin_client.get_rpc_server()
    balance = server.getbalance(os.environ['DOGE_ACCOUNT'])
    total_received = server.getreceivedbyaddress(faucet_address)
    dictionary['balance'] = balance
    dictionary['given_out'] = total_received - balance
    dictionary['give_amount'] = DOGE_AMOUNT
  except Exception as e:
    logging.error('dogecoin client error: ' + str(e))
    dictionary['error'] = 'couldn\'t connect to dogecoin :('
  return dictionary
