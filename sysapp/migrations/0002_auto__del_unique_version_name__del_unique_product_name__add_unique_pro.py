# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Product', fields ['name']
        db.delete_unique(u'sysapp_product', ['name'])

        # Removing unique constraint on 'Version', fields ['name']
        db.delete_unique(u'sysapp_version', ['name'])

        # Adding unique constraint on 'Product', fields ['version', 'name']
        db.create_unique(u'sysapp_product', ['version_id', 'name'])


    def backwards(self, orm):
        # Removing unique constraint on 'Product', fields ['version', 'name']
        db.delete_unique(u'sysapp_product', ['version_id', 'name'])

        # Adding unique constraint on 'Version', fields ['name']
        db.create_unique(u'sysapp_version', ['name'])

        # Adding unique constraint on 'Product', fields ['name']
        db.create_unique(u'sysapp_product', ['name'])


    models = {
        u'sysapp.dbserver': {
            'Meta': {'ordering': "['dbname']", 'unique_together': "(('dbname', 'dbport', 'dbhost'),)", 'object_name': 'DbServer'},
            'dbhost': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'dbname': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'dbpass': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'dbport': ('django.db.models.fields.IntegerField', [], {'default': '3306'}),
            'dbstatus': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'dbuser': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'dbserver'", 'to': u"orm['sysapp.Product']"})
        },
        u'sysapp.product': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('version', 'name'),)", 'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'version': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'product'", 'to': u"orm['sysapp.Version']"})
        },
        u'sysapp.project': {
            'Meta': {'ordering': "['name']", 'object_name': 'Project'},
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'})
        },
        u'sysapp.version': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('project', 'name'),)", 'object_name': 'Version'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'version'", 'to': u"orm['sysapp.Project']"})
        }
    }

    complete_apps = ['sysapp']