import os

from django.http import HttpResponse
from django.shortcuts import render
from django.template import RequestContext
from django.views.decorators.http import require_GET
from jsonrpclib import Server


@require_GET
def home(request):
  return render(request, 'base.html',
      dictionary={'faucet_addr': os.environ['FAUCET_ADDR']},
      context_instance=RequestContext(request))


def get_rpc_server():
  url = 'http://%s:%s@%s' % (os.environ['DOGEUSER'],
                             os.environ['DOGEPASS'],
                             os.environ['DOGESERVER'])
  return Server(url)
