from django.db import models

class Transaction(models.Model):
  ip_address = models.IPAddressField()
  sent_address = models.CharField(max_length=50)
  tx_time = models.DateTimeField()
