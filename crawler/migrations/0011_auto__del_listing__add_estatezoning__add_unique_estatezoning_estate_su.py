# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'Listing'
        db.delete_table('crawler_listing')

        # Adding model 'EstateZoning'
        db.create_table('crawler_estatezoning', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('estate', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.RealEstate'])),
            ('subdist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Subdistrict'])),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal('crawler', ['EstateZoning'])

        # Adding unique constraint on 'EstateZoning', fields ['estate', 'subdist']
        db.create_unique('crawler_estatezoning', ['estate_id', 'subdist_id'])

        # Deleting field 'Community.dist'
        db.delete_column('crawler_community', 'dist_id')

        # Deleting field 'Community.name'
        db.delete_column('crawler_community', 'name')

        # Adding field 'Community.detail'
        db.add_column('crawler_community', 'detail',
                      self.gf('django.db.models.fields.CharField')(max_length=255, null=True),
                      keep_default=False)


        # Changing field 'Community.desc'
        db.alter_column('crawler_community', 'desc', self.gf('django.db.models.fields.CharField')(default='', max_length=32))

        # Changing field 'RealEstate.area'
        db.alter_column('crawler_realestate', 'area', self.gf('django.db.models.fields.FloatField')(null=True))

        # Changing field 'RealEstate.nbedrm'
        db.alter_column('crawler_realestate', 'nbedrm', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'RealEstate.community'
        db.alter_column('crawler_realestate', 'community_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Community'], null=True))

        # Changing field 'RealEstate.facing'
        db.alter_column('crawler_realestate', 'facing', self.gf('django.db.models.fields.CharField')(max_length=8, null=True))

        # Changing field 'RealEstate.nlvnrm'
        db.alter_column('crawler_realestate', 'nlvnrm', self.gf('django.db.models.fields.IntegerField')(null=True))

        # Changing field 'RealEstate.desc'
        db.alter_column('crawler_realestate', 'desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # Changing field 'RealEstate.price'
        db.alter_column('crawler_realestate', 'price', self.gf('django.db.models.fields.FloatField')(null=True))

        # Renaming column for 'RealEstate.hlid' to match new field type.
        db.rename_column('crawler_realestate', 'hlid_id', 'hlid')
        # Changing field 'RealEstate.hlid'
        db.alter_column('crawler_realestate', 'hlid', self.gf('django.db.models.fields.CharField')(unique=True, max_length=64))
        # Removing index on 'RealEstate', fields ['hlid']
        db.delete_index('crawler_realestate', ['hlid_id'])

        # Adding unique constraint on 'RealEstate', fields ['hlid']
        db.create_unique('crawler_realestate', ['hlid'])


    def backwards(self, orm):
        # Removing unique constraint on 'RealEstate', fields ['hlid']
        db.delete_unique('crawler_realestate', ['hlid'])

        # Adding index on 'RealEstate', fields ['hlid']
        db.create_index('crawler_realestate', ['hlid_id'])

        # Removing unique constraint on 'EstateZoning', fields ['estate', 'subdist']
        db.delete_unique('crawler_estatezoning', ['estate_id', 'subdist_id'])

        # Adding model 'Listing'
        db.create_table('crawler_listing', (
            ('updated', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('subdist', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Subdistrict'])),
            ('time_added', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('hlid', self.gf('django.db.models.fields.CharField')(max_length=64, unique=True)),
        ))
        db.send_create_signal('crawler', ['Listing'])

        # Deleting model 'EstateZoning'
        db.delete_table('crawler_estatezoning')


        # User chose to not deal with backwards NULL issues for 'Community.dist'
        raise RuntimeError("Cannot reverse this migration. 'Community.dist' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'Community.name'
        raise RuntimeError("Cannot reverse this migration. 'Community.name' and its values cannot be restored.")
        # Deleting field 'Community.detail'
        db.delete_column('crawler_community', 'detail')


        # Changing field 'Community.desc'
        db.alter_column('crawler_community', 'desc', self.gf('django.db.models.fields.CharField')(max_length=255, null=True))

        # User chose to not deal with backwards NULL issues for 'RealEstate.area'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.area' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.nbedrm'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.nbedrm' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.community'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.community' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.facing'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.facing' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.nlvnrm'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.nlvnrm' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.desc'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.desc' and its values cannot be restored.")

        # User chose to not deal with backwards NULL issues for 'RealEstate.price'
        raise RuntimeError("Cannot reverse this migration. 'RealEstate.price' and its values cannot be restored.")

        # Renaming column for 'RealEstate.hlid' to match new field type.
        db.rename_column('crawler_realestate', 'hlid', 'hlid_id')
        # Changing field 'RealEstate.hlid'
        db.alter_column('crawler_realestate', 'hlid_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['crawler.Listing']))

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
