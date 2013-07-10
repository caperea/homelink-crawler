# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'RealEstate'
        db.create_table('crawler_realestate', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hlid', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('nbedrm', self.gf('django.db.models.fields.IntegerField')()),
            ('nlvnrm', self.gf('django.db.models.fields.IntegerField')()),
            ('area', self.gf('django.db.models.fields.FloatField')()),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('facing', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('in_sale', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('duty_free', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('edu_district', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('crawler', ['RealEstate'])

        # Adding model 'Community'
        db.create_table('crawler_community', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('district', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('addr', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('link', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64)),
            ('desc', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('time_updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal('crawler', ['Community'])


    def backwards(self, orm):
        # Deleting model 'RealEstate'
        db.delete_table('crawler_realestate')

        # Deleting model 'Community'
        db.delete_table('crawler_community')


    models = {
        'crawler.community': {
            'Meta': {'object_name': 'Community'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'district': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'crawler.realestate': {
            'Meta': {'object_name': 'RealEstate'},
            'area': ('django.db.models.fields.FloatField', [], {}),
            'duty_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edu_district': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facing': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hlid': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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