#!-*- coding: utf8 -*-
from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import DbAction, DbActionRes
from django.contrib.auth import get_user_model
from sysapp.models import Project, DbServer
from common import ssh_command, Dict, mysql_select
import itertools
import xlwt
import json
import time
import datetime
import re

def _setting_dbsearch_data(request, data):
    '''
        now = timezone.now()
        start = now - datetime.timedelta(hours=23, minutes=59, seconds=59)
        today_topic = Topic.objects.filter(created_on__gt=start)

    '''
    kw = {}
    data['sub_template'] = 'tablepage/dbsearch.html'
    req_value = {}
    for k, v in request.GET.items():
        req_value[k] = str(v).strip()
    execute_status = req_value.get('execute_status', '')
    title          = req_value.get(u'title', '')
    user           = req_value.get(u'user', '')
    time_start     = req_value.get('time_start', '')
    time_end       = req_value.get('time_end', '')
    if execute_status:
        kw['execute_status'] = execute_status
    if title:
        kw['title__contains'] = title
    if user:
        kw['user__name'] = user
    if time_start:
        time_start = datetime.datetime.strptime(time_start, "%Y-%m-%d %H:%M")
        kw['datetime__gt'] = time_start
    if time_end:
        time_end = datetime.datetime.strptime(time_end, "%Y-%m-%d %H:%M")
        kw['datetime__lt'] = time_end
    data['reqval'] = req_value
    data['posts'] = DbAction.objects.filter(**kw)
    return data


def _setting_appaction_data(request, data):
    data['posts'] = ''
    data['sub_template'] = 'tablepage/appaction.html'
    return data


def appaction_ajax(request):
    data = {}
    if len(request.POST) != 0:
        ssh_param = Dict(('username', 'password', 'host', 'port', 'command'), ('' for i in range(5)))
        for k, v in ssh_param.iteritems():
            if k == 'port': 
                ssh_param[k] = int(request.POST.get(k, 22))
                continue
            ssh_param[k] = str(request.POST.get(k, '')).strip()
        print ssh_param
#        for k in itertools.ifilterfalse(lambda k: ssh_param[k] != '', ssh_param.keys()):
#            data['rrors'] = '%s is empty' % k
#            return data
        ssh_res = ssh_command(**ssh_param)
        print ssh_res
        stdout, stderr = ssh_res
        if stderr:
            data['res'] = stderr
            data['act'] = 'stderr'
        else:
            data['res'] = stdout
            data['act'] = 'stdout'
        return HttpResponse(json.dumps(data), content_type="application/json")



def _setting_dbselect_data(request, data):
    data['posts'] = ''
    data['sub_template'] = 'tablepage/dbselect.html'
    return data



def _setting_dbaction_data(request, data):
    kw = {}
    data['sub_template'] = 'tablepage/dbactionlist.html'
    instance = get_user_model().objects.get(pk=request.user.id)
    if 'execute_status' in request.GET: kw['execute_status'] = request.GET.get('execute_status', 0)
    if instance.is_superuser == 1:
        dbaction = DbAction.objects.select_related().filter(**kw).order_by('-datetime')
    else:
        dbaction = DbAction.objects.filter(user=instance, **kw).order_by('-datetime')
    data['posts'] = dbaction    
    return data


def dbaction_ajax(request, id=None, execute_status=None):
    if not request.user.is_superuser:
        raise Http404
    if id and execute_status:
        instance = DbAction.objects.get(pk=id)
#        DbActionRes.objects.filter(dbaction=instance).update(execute_status=execute_status)
        instance.execute_status = execute_status
        instance.save()
        data = {'status': True, 'action': 'reload'}
        return HttpResponse(json.dumps(data), content_type="application/json")


def dbselect_ajax(request):
    all_tree = []
    for project in Project.objects.all():
        project_tree = {"n": project.name, "s": []}
        for v in  project.version.all():
            version_tree = {"n": v.name, "s": []}
            project_tree['s'].append(version_tree)
            for p in v.product.all():
                product_tree = {"n": p.name, "s": []}
                version_tree['s'].append(product_tree)
                for d in p.dbserver.all():
                    dbserver_tree = {"n": d.db_format(), "s": []}
                    product_tree['s'].append(dbserver_tree)
        all_tree.append(project_tree)
    return HttpResponse(json.dumps(all_tree))


def db_select_ajax(request):
    import mysql.connector
    sql = request.GET.get('sql', False)
    if sql:
        if not re.match('select',sql, flag=re.IGNORECASE): return HttpResponse('')


def db_tables_ajax(request):
    import mysql.connector
    data = {'act': '', 'res':''}
    dbstring = request.GET.get('dbstr', '')
    if dbstring.count(':') != 2:
        data['act'] = 'show'
        data['res'] = 'database format error %s' % dbstring
        return HttpResponse(json.dumps(data))
    dbname, dbhost, dbport = dbstring.split(':')
    try:
        dbserver = DbServer.objects.get(dbname=dbname, dbhost=dbhost, dbport=dbport, dbstatus=1)
    except:
        data['act'] = 'show'
        data['res'] = 'Connect fail'
        return HttpResponse(json.dumps(data))
    dbpass = dbserver.dbpass
    dbuser = dbserver.dbuser
    cnx = mysql.connector.connect(user=dbuser, database=dbname, host=dbhost, password=dbpass, port=dbport)
    cursor = cnx.cursor()
    sql = request.GET.get('sql', False)
    print sql
    if sql:
        sql = sql.strip()
        if not re.match('select', sql, flags=re.IGNORECASE):
            data['act'] = 'stderr'
            data['res'] = 'SQL must be select'
            return HttpResponse(json.dumps(data))
        vertical = request.GET.get('vertical', 'default')
        stdout, stderr = mysql_select(
                                    dbhost=dbhost,
                                    dbuser=dbuser,
                                    dbpass=dbpass,
                                    dbport=dbport,
                                    dbname=dbname,
                                    sql=sql,
                                    html=False,
                                    vertical=True if vertical == 'vertical' else False,
                                )
        if stderr:
            data['res'] = stderr
            data['act'] = 'stderr'
        else:
            data['res'] = stdout
            data['act'] = 'stdout'
        return HttpResponse(json.dumps(data))
    cursor.execute("show tables")
    tables = ''
    for table in cursor:
        tables += str(table[0]) + ";"
    print tables
    cursor.close()
    cnx.close()
    data['act'] = 'show'
    data['res'] = tables
    return HttpResponse(json.dumps(data))


def modal_sql_script(request):
    data = {}
    print request
    if request.method == 'POST':
        print request.FILES['file']
        return 
    return render(request, 'formpage/modal_sql_form.html', data) 


def modal_detail(request, id=None):
    instance = DbActionRes.objects.get(pk=id)
    data = {'dbactionres': instance}
    return render(request, 'formpage/modal_detail.html', data) 



def excel_output(self):
    dbaction = DbAction.objects.all()
    _lst = []
    for d in dbaction:
        status = ''
        if d.execute_status == 0:
            status = u'待审核'
        elif d.execute_status == 1:
            status = u'已撤销'
        elif d.execute_status == 2:
            status = u'已通过'
        dlist = [d.db.get_db_info(), d.title, d.sql, status, d.user.get_full_name(), str(d.datetime)]
        _lst.append(dlist)
    _lst.insert(0, [u'数据库', u'变更标题', u'SQL语句', u'申请状态', u'申请人', u'申请时间'])
    book = xlwt.Workbook(encoding='utf8')
    sheet = book.add_sheet(u'DB变更记录')
    for row, d in enumerate(_lst):
        for col, val in enumerate(d):
            sheet.write(row, col, val, style=xlwt.Style.default_style)  
    response = HttpResponse(mimetype='application/vnd.ms-excel')  
    response['Content-Disposition'] = 'attachment; filename=example-%s.xls' % (time.strftime('%Y-%m-%d-%H-%M')) 
    book.save(response)  
    return response  

