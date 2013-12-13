from django.contrib import admin
from faucet.models import Transaction

class TransactionAdmin(admin.ModelAdmin):
  list_display = ('ip_address', 'sent_address', 'tx_time')

admin.site.register(Transaction, TransactionAdmin)
