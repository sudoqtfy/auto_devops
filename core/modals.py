from django.shortcuts import render as render_views, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from .forms import create_core_form
from django.contrib.auth import get_user_model
import json


_user = get_user_model()



class ModalPermissionException(Exception):
    pass


def modal_form(request, form_name, id=None, parent_name=None, parent_id=None, app=None):
    try:
        return _get_app_modal(app, form_name)(id, form_name).render(request)
    except ModalPermissionException:
        return HttpResponse({'status': False, 'message':'Access forbidden'}, content_type="application/json", status=403)


def modal_delete(request, form_name, id, app='core'):
    try:
        return _get_app_modal(app, form_name)(id, form_name).delete(request)
    except ModalPermissionException:
        return HttpResponse({'status': False, 'message':'Access forbidden'}, content_type="application/json", status=403)


def _get_app_modal(app, form_name):
    if not app:
        app = 'core'
    if app in settings.INSTALLED_APPS:
        obj = __import__(app, fromlist=['modals']).modals
        try:
            obj = getattr(obj, '%sModal' % form_name.title())
        except AttributeError:
            raise Http404()
    else:
        raise Http404()
    return obj



class Modal(object):
    form = None

    def __init__(self, id, form_name):
        self.data =  {'status': True, 'action': 'reload'}
        self.id = id
        self.form_name = form_name

    def create_form(self):
        pass

    def render(self, request):
        self.request = request
        self.create_form()
        template = 'formpage/modal_form.html'
        if request.method == "POST":
            template = 'formpage/sub_form.html'
#            template = 'formpage/%s_form.html' % self.form_name
            if self.form.is_valid():
                try:
                    self.before_save()
                    self.form.save()
                    return HttpResponse(json.dumps(self.data), content_type="application/json")
                except Exception, e:
                    print str(e)
#        self.data['form_template'] = 'formpage/%s_form.html' % self.form_name
        self.data['form_template'] = 'formpage/sub_form.html'
        self.data['request_path'] = request.path
        self.data['form'] = self.form
        self.data['section'] = self.form_name
        return render_views(request, template, self.data)


    def before_save(self):
        pass

    def save(self):
        pass

    def delete(self, request):
        self.request = request
        self.create_form()
        self.instance = get_object_or_404(self.form.Meta.model, pk=self.id)
        self.instance.delete()
        return HttpResponse(json.dumps(self.data), content_type="application/json")
    



class BaseCoreModal(Modal):

    def create_form(self):
        self.form = create_core_form(self.id, self.request.POST, self.form_name)


class UserModal(BaseCoreModal):
    
    def before_save(self):
        instance = self.form.instance
        instance.username = instance.email
        if len(instance.password):
            instance.set_password(instance.password)
        else:
            instance.password = _user.objects.get(pk=instance.id).password
        
   


def get_modal_form(app, form_name):
    if app not in settings.INSTALLED_APPS:
        app = 'core'
    obj = __import__(app, fromlist=['modals'])
    print obj
    return ''

