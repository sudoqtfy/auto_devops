# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Project'
        db.create_table(u'sysapp_project', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal(u'sysapp', ['Project'])

        # Adding model 'Version'
        db.create_table(u'sysapp_version', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('project', self.gf('django.db.models.fields.related.ForeignKey')(related_name='version', to=orm['sysapp.Project'])),
        ))
        db.send_create_signal(u'sysapp', ['Version'])

        # Adding unique constraint on 'Version', fields ['project', 'name']
        db.create_unique(u'sysapp_version', ['project_id', 'name'])

        # Adding model 'Product'
        db.create_table(u'sysapp_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=128)),
            ('version', self.gf('django.db.models.fields.related.ForeignKey')(related_name='product', to=orm['sysapp.Version'])),
        ))
        db.send_create_signal(u'sysapp', ['Product'])

        # Adding model 'DbServer'
        db.create_table(u'sysapp_dbserver', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('dbname', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('dbhost', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('dbport', self.gf('django.db.models.fields.IntegerField')(default=3306)),
            ('dbuser', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('dbpass', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(related_name='dbserver', to=orm['sysapp.Product'])),
            ('dbstatus', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'sysapp', ['DbServer'])

        # Adding unique constraint on 'DbServer', fields ['dbname', 'dbport', 'dbhost']
        db.create_unique(u'sysapp_dbserver', ['dbname', 'dbport', 'dbhost'])


    def backwards(self, orm):
        # Removing unique constraint on 'DbServer', fields ['dbname', 'dbport', 'dbhost']
        db.delete_unique(u'sysapp_dbserver', ['dbname', 'dbport', 'dbhost'])

        # Removing unique constraint on 'Version', fields ['project', 'name']
        db.delete_unique(u'sysapp_version', ['project_id', 'name'])

        # Deleting model 'Project'
        db.delete_table(u'sysapp_project')

        # Deleting model 'Version'
        db.delete_table(u'sysapp_version')

        # Deleting model 'Product'
        db.delete_table(u'sysapp_product')

        # Deleting model 'DbServer'
        db.delete_table(u'sysapp_dbserver')


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
            'Meta': {'ordering': "['name']", 'object_name': 'Product'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
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
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '128'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'version'", 'to': u"orm['sysapp.Project']"})
        }
    }

    complete_apps = ['sysapp']