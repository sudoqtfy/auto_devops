#!-*- coding: utf8 -*-
from django.test import TestCase
from dbapp.models import DbAction
from sysapp.models import *
from django.db import connection
from django.http import HttpResponse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
import json
# Create your tests here.

@login_required
def echarts(request):
    dbaction_status = []
    reg_user = []
    db_status = []
    data = dict()
    all_tree =  {"name": u"项目图表", "children": []}
    ### sql execute status
    for i in [2, 1, 0]:
        dbaction_status.append(DbAction.objects.filter(execute_status=i).count())
    ### reg user
    for i in [True, False]:
        reg_user.append(get_user_model().objects.filter(is_superuser=i).count())
    ### db connect status
    for i in [0, 1, 2]:
        db_status.append(DbServer.objects.filter(dbstatus=i).count())

    data ={'dbaction_status':[
                {'value': dbaction_status[0], 'name':u'已通过'},
                {'value': dbaction_status[1], 'name':u'已取消'},
                {'value': dbaction_status[2], 'name':u'待审核'},
            ],
            'all_tree': [all_tree],
            'reg_user': [
                {'value': reg_user[0], 'name':u'管理员'},
                {'value': reg_user[1], 'name':u'普通用户'},
            ],
            'db_status':[
                {'value': db_status[0], 'name':u'正在连接'},
                {'value': db_status[1], 'name':u'连接成功'},
                {'value': db_status[2], 'name':u'连接失败'},
            ],
        }
    for project in Project.objects.all():
        project_tree = {"name": project.name, "children": []}
        for v in  project.version.all():
            version_tree = {"name": v.name, "children": []}
            project_tree['children'].append(version_tree)
            for p in v.product.all():
                product_tree = {"name": p.name, "children": []}
                version_tree['children'].append(product_tree)
                for d in p.dbserver.all():
                    dbserver_tree = {"name": str(d), "children": []}
                    product_tree['children'].append(dbserver_tree)
        all_tree['children'].append(project_tree)
    return HttpResponse(json.dumps(data))
