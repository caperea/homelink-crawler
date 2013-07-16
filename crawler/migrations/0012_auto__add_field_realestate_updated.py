# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'RealEstate.updated'
        db.add_column('crawler_realestate', 'updated',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'RealEstate.updated'
        db.delete_column('crawler_realestate', 'updated')


    models = {
        'crawler.community': {
            'Meta': {'object_name': 'Community'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'detail': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'crawler.district': {
            'Meta': {'object_name': 'District'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crawler.estatezoning': {
            'Meta': {'unique_together': "(('estate', 'subdist'),)", 'object_name': 'EstateZoning'},
            'estate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.RealEstate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Subdistrict']"}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
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