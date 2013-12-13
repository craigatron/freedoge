import logging
import os
from faucet import dogecoin_client

def template_constants(request):
  faucet_address = os.environ['FAUCET_ADDR']
  dictionary = {'FAUCET_ADDR': faucet_address}
  if settings.ANALYTICS_ID:
    dictionary['ANALYTICS_ID'] = settings.ANALYTICS_ID
  try:
    server = dogecoin_client.get_rpc_server()
    balance = server.getbalance(os.environ['DOGE_ACCOUNT'])
    total_received = server.getreceivedbyaddress(faucet_address)
    dictionary['balance'] = balance
    dictionary['given_out'] = total_received - balance
  except Exception as e:
    logging.error('dogecoin client error: ' + str(e))
    dictionary['error'] = 'couldn\'t connect to dogecoin :('
  return dictionary
