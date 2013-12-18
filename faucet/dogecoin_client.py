import os
from bitcoinrpc.authproxy import AuthServiceProxy

def get_rpc_server():
  url = 'http://%s:%s@%s' % (os.environ['DOGEUSER'],
                             os.environ['DOGEPASS'],
                             os.environ['DOGESERVER'])
  return AuthServiceProxy(url)
