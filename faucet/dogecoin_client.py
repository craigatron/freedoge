import os
from jsonrpclib import Server

def get_rpc_server():
  url = 'http://%s:%s@%s' % (os.environ['DOGEUSER'],
                             os.environ['DOGEPASS'],
                             os.environ['DOGESERVER'])
  return Server(url)
