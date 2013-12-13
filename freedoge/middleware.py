from django.conf import settings
from django.http import HttpResponse

class MaintenanceMiddleware(object):
  def process_request(self, request):
    if settings.MAINTENANCE:
      return HttpResponse('down for maintenance :(')
    return None
