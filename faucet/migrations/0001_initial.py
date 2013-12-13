# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Transaction'
        db.create_table(u'faucet_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_address', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('sent_address', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('tx_time', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal(u'faucet', ['Transaction'])


    def backwards(self, orm):
        # Deleting model 'Transaction'
        db.delete_table(u'faucet_transaction')


    models = {
        u'faucet.transaction': {
            'Meta': {'object_name': 'Transaction'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'sent_address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'tx_time': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['faucet']