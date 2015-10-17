from django.db import models
from django.core.validators import RegexValidator
from django.db.models.signals import post_delete, post_save
import pgcrypto
import subprocess

# Create your models here.

def validate_name():
        return RegexValidator(regex='^[a-zA-Z0-9_\.\-]+$', message='Invalid characters')


class Project(models.Model):
    name = models.CharField(blank=False, max_length=128, validators=[validate_name()], unique=True)
    description = models.CharField(blank=True, max_length=255)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return self.name


class Version(models.Model):
    name = models.CharField(blank=False, max_length=128, validators=[validate_name()])
    project = models.ForeignKey(Project, related_name="version")

    class Meta:
        ordering = ['name']
        unique_together = ('project', 'name')

    def __unicode__(self):
        try:
            return '%s->%s' % (self.name, getattr(self, 'project'))
        except:
            return self.name



class Product(models.Model):
    name = models.CharField(blank=False, max_length=128, validators=[validate_name()])
    version = models.ForeignKey(Version, related_name="product")

    class Meta:
        ordering = ['name']
        unique_together = ('version', 'name')

    def __unicode__(self):
        try:
            return '%s->%s' % (self.name, getattr(self, 'version'))
        except:
            return self.name


class DbServer(models.Model):
    STATUS_CHOICES = (
            (0, 'Connecting'),
            (1, 'connect success'),
            (2,'connect failure'),
    )
    dbname = models.CharField(blank=False, max_length=128, validators=[validate_name()])
    dbhost = models.CharField(blank=False, max_length=128)
    dbport = models.IntegerField(blank=False, default=3306)
    dbuser = models.CharField(blank=False, max_length=128) 
    dbpass = pgcrypto.EncryptedTextField(blank=True)
    product = models.ForeignKey(Product, related_name='dbserver')
    dbstatus = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="db connect status")

    class Meta:
        ordering = ['dbname']
        unique_together = ('dbname', 'dbport', 'dbhost')

    def __unicode__(self):
        return '%s[%s:%s]' % (self.dbname, self.dbhost, self.dbport)

    def get_db_info(self):
        return '%s[%s:%s]' % (self.dbname, self.dbhost, self.dbport)

    def db_format(self):
        return '%s:%s:%s' % (self.dbname, self.dbhost, self.dbport)

    @staticmethod
    def on_save_dbserver(sender, instance, created, **kwargs):
        from sysapp.tasks import try_connect_mysql
        data = {
                'host': instance.dbhost,
                'user': instance.dbuser,
                'password': instance.dbpass if instance.dbpass else 'root',
                'port': instance.dbport,
                'database': instance.dbname,
                'id': instance.id,
                }
        print data
        try_connect_mysql.delay(**data)
#        if status:
#            DbServer.objects.filter(id=instance.id).update(dbstatus=1)
#        else:
#            DbServer.objects.filter(id=instance.id).update(dbstatus=2)
#        cmd = "/usr/local/mysql/bin/mysqladmin  -h %(dbhost)s -u%(dbname)s -p%(dbpass)s ping | grep -c alive" % data

#        ret = subprocess.call(cmd, shell=True)
        

post_save.connect(DbServer.on_save_dbserver, sender=DbServer)

#class DbAuthentication(models.Model):
#    dbserver = models.OneToOneField(DbServer, primary_key=True)



