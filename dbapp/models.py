from django.db import models
from sysapp.models import DbServer
from django.utils import timezone
from django.db.models.signals import post_delete, post_save
from django.contrib.auth import get_user_model
import copy

_user = get_user_model()

class DbAction(models.Model):
    PENDING = 0
    REJECT  = 1
    ALLOWED = 2
    STATUS_CHOICES = (
        (PENDING, 'PENDING'),
        (REJECT, 'REJECT'),
        (ALLOWED, 'ALLOWED'),
    )
    db = models.ForeignKey(DbServer, related_name='db')
    user = models.ForeignKey(_user, related_name='user')
    title = models.CharField(blank=False, max_length=255)
    sql = models.TextField(blank=False)
    datetime = models.DateTimeField(auto_now_add=True)
    execute_status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    class Meta:
        ordering = ['db']

    def __unicode__(self):
        return self.title


    @staticmethod
    def on_create_dbaction(sender, instance, created, **kwargs):
        from core.tasks import SendEmailTask
        from dbapp.tasks import EmailMsg
        email_msg = EmailMsg(instance)
#        print email_msg.get_msg_html()
#        print email_msg.get_msg_text()
#        print email_msg.get_subject_text()
        if created:
            DbActionRes(dbaction=instance).save()
            admins = _user.objects.filter(is_superuser=True)
            for admin in admins:
                SendEmailTask().delay(subject=email_msg.get_subject_text(),
                                    message=email_msg.get_msg_text(),
                                    message_html=email_msg.get_msg_html(),
                                    recipient=admin.email)

        if not created and int(instance.execute_status) == 0:
            admins = _user.objects.filter(is_superuser=True)
            for admin in admins:
                SendEmailTask().delay(subject=email_msg.get_subject_text(),
                                    message=email_msg.get_msg_text(),
                                    message_html=email_msg.get_msg_html(),
                                    recipient=admin.email)

        if int(instance.execute_status) == 2:
            from .tasks import execute_dml
            sqlstring = instance.sql
            host      = instance.db.dbhost
            user      = instance.db.dbuser
            password  = instance.db.dbpass
            port      = instance.db.dbport
            database  = instance.db.dbname
            execute_dml.delay(
                        user=user,
                        password=password,
                        database=database,
                        host=host,
                        port=port,
                        sqlstring=sqlstring,
                        id=instance.dbactionres.id,
                        autocommit=True,
                )


#            SendEmailTask().apply_async(kwargs=dict(subject=email_msg.get_subject_text(),
#                                  message=email_msg.get_msg_text(),
#                                  message_html=email_msg.get_msg_html(),
#                                  recipient=instance.user.email
#                                  ),
#                                  countdown=10)


        if int(instance.execute_status) == 1:
            SendEmailTask().delay(subject=email_msg.get_subject_text(),
                                  message=email_msg.get_msg_text(),
                                  message_html=email_msg.get_msg_html(),
                                  recipient=instance.user.email)


post_save.connect(DbAction.on_create_dbaction, sender=DbAction)

class DbActionRes(models.Model):
    dbaction = models.OneToOneField(DbAction)
    execute_result = models.TextField()
    class Meta:
        ordering = ['dbaction']

    def __unicode__(self):
        return self.dbaction

    @staticmethod
    def on_save_dbactionres(sender, instance, created, **kwargs):
        if not created and instance.execute_result:
            from core.tasks import SendEmailTask
            from dbapp.tasks import EmailMsg
            print instance.dbaction.execute_status
            instance_copy = copy.deepcopy(instance)
            instance_copy.execute_status = str(instance.dbaction.execute_status)
            instance_copy.datetime = instance.dbaction.datetime
            instance_copy.sql = instance.dbaction.sql
            instance_copy.user = instance.dbaction.user
            email_msg = EmailMsg(instance_copy)
            SendEmailTask().delay(subject=email_msg.get_subject_text(),
                               message=email_msg.get_msg_text(),
                               message_html=email_msg.get_msg_html(),
                               recipient=instance_copy.user.email,
                               )

post_save.connect(DbActionRes.on_save_dbactionres, sender=DbActionRes)
