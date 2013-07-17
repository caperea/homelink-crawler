# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'EstateZoning', fields ['estate', 'subdist']
        db.delete_unique('crawler_estatezoning', ['estate_id', 'subdist_id'])

        # Deleting model 'EstateZoning'
        db.delete_table('crawler_estatezoning')


    def backwards(self, orm):
        # Adding model 'EstateZoning'
        db.create_table('crawler_estatezoning', (
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.RealEstate'])),
            ('subdist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Subdistrict'])),
        ))
        db.send_create_signal('crawler', ['EstateZoning'])

        # Adding unique constraint on 'EstateZoning', fields ['estate', 'subdist']
        db.create_unique('crawler_estatezoning', ['estate_id', 'subdist_id'])


    models = {
        'crawler.community': {
            'Meta': {'object_name': 'Community'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '32', 'null': 'True'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'crawler.district': {
            'Meta': {'object_name': 'District'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crawler.realestate': {
            'Meta': {'object_name': 'RealEstate'},
            'area': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'community': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Community']", 'null': 'True'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'duty_free': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'edu_district': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'facing': ('django.db.models.fields.CharField', [], {'max_length': '8', 'null': 'True'}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_sale': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'nbedrm': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'nlvnrm': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'price': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'subdist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Subdistrict']"}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'crawler.subdistrict': {
            'Meta': {'object_name': 'Subdistrict'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'dist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.District']"}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '8'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'updated': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['crawler']