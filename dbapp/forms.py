#!-*- coding: utf8 -*-
from core.forms import ModalForm, create_form
from .models import DbAction
from django.forms.widgets import Textarea, SelectMultiple, HiddenInput, TextInput, PasswordInput



class DbActionForm(ModalForm):

    def __init__(self, *args, **kwargs):
        super(DbActionForm, self).__init__(*args, **kwargs)
        self.fields['db'].label = u'数据库'
        self.fields['sql'].label = u'sql语句'
        self.fields['title'].label = u'变更标题'

    class Meta:
        model = DbAction
        fields = ['db', 'title', 'sql']
        widgets = {'sql': Textarea(attrs={'cols': 10 ,'rows': 18})}



def create_dbapp_form(id=None, request_data=None, form_name='user', app=None, kwargs={}):
    form_pattern = {
        'dbaction': DbActionForm,
    }
    return create_form(form_pattern, id, request_data, form_name, kwargs)
