# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Listing'
        db.create_table('crawler_listing', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hlid', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('updated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('crawler', ['Listing'])


        # Renaming column for 'RealEstate.hlid' to match new field type.
        db.rename_column('crawler_realestate', 'hlid', 'hlid_id')
        # Changing field 'RealEstate.hlid'
        db.alter_column('crawler_realestate', 'hlid_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Listing']))
        # Adding index on 'RealEstate', fields ['hlid']
        db.create_index('crawler_realestate', ['hlid_id'])


    def backwards(self, orm):
        # Removing index on 'RealEstate', fields ['hlid']
        db.delete_index('crawler_realestate', ['hlid_id'])

        # Deleting model 'Listing'
        db.delete_table('crawler_listing')


        # Renaming column for 'RealEstate.hlid' to match new field type.
        db.rename_column('crawler_realestate', 'hlid_id', 'hlid')
        # Changing field 'RealEstate.hlid'
        db.alter_column('crawler_realestate', 'hlid', self.gf('django.db.models.fields.CharField')(max_length=64))

    models = {
        'crawler.community': {
            'Meta': {'object_name': 'Community'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'crawler.listing': {
            'Meta': {'object_name': 'Listing'},
            'hlid': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'crawler.realestate': {
            'Meta': {'object_name': 'RealEstate'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Community']"}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'duty_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edu_district': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facing': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hlid': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Listing']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sale': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'nbedrm': ('django.db.models.fields.IntegerField', [], {}),
            'nlvnrm': ('django.db.models.fields.IntegerField', [], {}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['crawler']