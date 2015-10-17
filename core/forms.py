#!-*- coding: utf8 -*-
from django.forms import ModelForm, ModelMultipleChoiceField, CharField, BooleanField
from django.forms.widgets import Textarea, SelectMultiple, HiddenInput, TextInput, PasswordInput
from crispy_forms.helper import FormHelper
from django.http import Http404
from django.conf import settings
from django.contrib.auth import get_user_model
_user = get_user_model()



class ModalForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ModalForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-sm-3'
        self.helper.field_class = 'col-sm-7'
        self.helper.label_size = ' col-sm-offset-3'




class UserForm(ModalForm):
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["email"] = CharField(required=True, label=u"电子邮件")
        self.fields["is_superuser"] = BooleanField(required=False)
        self.fields["password"] = CharField(widget=PasswordInput(render_value=False), required=False, min_length=8, label="密码")
        self.fields["name"] = CharField(label=u'用户名')


    class Meta:
        model = _user
        fields = ['email', 'password', 'name', 'qq', 'phone', 'is_superuser']



def create_form(form_pattern, id, request_data, form_name, kwargs):
    if form_name not in form_pattern: raise Http404
    if id:
        instance = form_pattern[form_name].Meta.model.objects.get(pk=id)
        print instance
    else:
        instance = form_pattern[form_name].Meta.model(**kwargs)
        print instance
    form = form_pattern[form_name](request_data or None, instance=instance)
    return form


def create_core_form(id=None, request_data=None, form_name='user', kwargs={}):
    form_pattern = {
        'user': UserForm,
    }
    return create_form(form_pattern, id, request_data, form_name, kwargs)
    

