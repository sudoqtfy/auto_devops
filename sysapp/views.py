from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Project, Version, Product, DbServer




def _setting_user_data(request, data):
    data['sub_template'] = 'tablepage/userlist.html'
    data['posts'] = get_user_model().objects.all().order_by('date_joined')
    return data


def _setting_project_data(request, data):
    data['sub_template'] = 'tablepage/projectlist.html'
    data['posts'] = Project.objects.all()
    return data


def _setting_version_data(request, data):
    data['sub_template'] = 'tablepage/versionlist.html'
    data['posts'] = Version.objects.all()
    return data


def _setting_product_data(request, data):
    data['sub_template'] = 'tablepage/productlist.html'
    data['posts'] = Product.objects.all()
    return data


def _setting_dbserver_data(request, data):
    data['sub_template'] = 'tablepage/dbserverlist.html'
    data['posts'] = DbServer.objects.all()
    return data

