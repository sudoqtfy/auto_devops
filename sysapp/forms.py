#!-*- coding: utf8 -*-
from core.forms import ModalForm, create_form
from .models import (Project, Version, Product, DbServer)
from django.forms import ModelForm, ModelMultipleChoiceField, CharField, BooleanField
from django.forms.widgets import Textarea, SelectMultiple, HiddenInput, TextInput, PasswordInput



class ProjectForm(ModalForm):
    
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.fields["name"] = CharField(label=u'项目名称')
        self.fields["description"] = CharField(label=u'项目说明', widget=Textarea(attrs={'rows': 5}))

    class Meta:
        model = Project
        fields = ['name', 'description']
#        widgets = {'description': Textarea(attrs={'rows': 5})}


class VersionForm(ModalForm):
    
    def __init__(self, *args, **kwargs):
        super(VersionForm, self).__init__(*args, **kwargs)
        self.fields["name"] = CharField(label=u'版本名称')
        self.fields['project'].label = '所属项目'

    class Meta:
        model = Version
        fields = ['name', 'project']


class ProductForm(ModalForm):
    
    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields["name"] = CharField(label=u'产品名称')
        self.fields['version'].label = u'所属版本'

    class Meta:
        model = Product
        fields = ['name', 'version']


class DbServerForm(ModalForm):
    '''
        queue = forms.ModelChoiceField(label=u'队列',queryset=Queue.objects.all())
        class ServerForm(forms.Form):
            queue = forms.ChoiceField(label=u'队列')
        def __init__(self,*args,**kwargs):
            super(ServerForm,self).__init__(*args,**kwargs)
            self.fields['queue'].choices=((x.que,x.disr) for x in Queue.objects.all())

    '''
    
    def __init__(self, *args, **kwargs):
        super(DbServerForm, self).__init__(*args, **kwargs)
        self.fields["dbname"] = CharField(label=u'数据库名')
        self.fields["dbhost"] = CharField(label=u'主机地址')
        self.fields["dbport"] = CharField(label=u'端口')
        self.fields["dbuser"] = CharField(label=u'用户名')
#        self.fields["dbpass"] = CharField(label=u'密码', widget=PasswordInput, required=True)
        self.fields["dbpass"] = CharField(label=u'密码', widget=PasswordInput)
#        self.fields["dbpass"] = CharField(label=u'密码')
        self.fields['product'].label = u'所属产品'

    class Meta:
        model = DbServer
        fields = ['dbname', 'dbhost', 'dbport', 'dbuser', 'dbpass', 'product']




def create_sysapp_form(id=None, request_data=None, form_name='user', app=None, kwargs={}):
    form_pattern = {
        'project': ProjectForm,
        'version': VersionForm,
        'product': ProductForm,
        'dbserver': DbServerForm,
    }
    return create_form(form_pattern, id, request_data, form_name, kwargs)

