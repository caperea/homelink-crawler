# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Listing.time_updated'
        db.delete_column('crawler_listing', 'time_updated')

        # Adding field 'Listing.subdist'
        db.add_column('crawler_listing', 'subdist',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['crawler.Subdistrict']),
                      keep_default=False)


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Listing.time_updated'
        raise RuntimeError("Cannot reverse this migration. 'Listing.time_updated' and its values cannot be restored.")
        # Deleting field 'Listing.subdist'
        db.delete_column('crawler_listing', 'subdist_id')


    models = {
        'crawler.community': {
            'Meta': {'object_name': 'Community'},
            'addr': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True'}),
            'dist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Subdistrict']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'time_updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'crawler.district': {
            'Meta': {'object_name': 'District'},
            'desc': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'crawler.listing': {
            'Meta': {'object_name': 'Listing'},
            'hlid': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'subdist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['crawler.Subdistrict']"}),
            'time_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
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