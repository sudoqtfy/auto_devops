from django.shortcuts import render as render_views, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import Http404, HttpResponse
from .forms import create_sysapp_form
from django.contrib.auth import get_user_model
import json
from core.modals import Modal




class BaseSysappModal(Modal):

    def create_form(self):
        self.form = create_sysapp_form(self.id, self.request.POST, self.form_name)


class ProductModal(BaseSysappModal):
    pass


class VersionModal(BaseSysappModal):
    pass


class ProjectModal(BaseSysappModal):
    pass

        
class DbserverModal(BaseSysappModal):
    pass
