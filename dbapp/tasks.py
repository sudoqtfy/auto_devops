#!-*- coding: utf8 -*-
from auto_devops.celery import app
import sys
import re
import string
import json
from django.template import TemplateDoesNotExist
from django.template.loader import render_to_string
try:
    import cPickle as pickle
except ImportErro:
    import pickle

@app.task()
def execute_dml(user='root', password='root', database='tmp', host='127.0.0.1', port=3306, sqlstring=None, id=None, **kw):
    if not sqlstring: return
    import mysql.connector
    from mysql.connector import errorcode
    from dbapp.models import DbActionRes
    from core.tasks import SendEmailTask
    params = dict(user=user, password=password, database=database, host=host, port=port)
    defaults = dict(use_unicode=True, charset='utf8', collation='utf8_general_ci', autocommit=False)
    for k, v in defaults.iteritems():
        params[k] = kw.pop(k, v)
    params.update(kw)
    ### try connect
    try:
        conn = mysql.connector.connect(**params)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            res = "Something is wrong with your user name or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            res = "Database does not exist"
        else:
            res = str(err)
        dbactionres = DbActionRes.objects.get(pk=id)
        dbactionres.execute_result = pickle.dumps([dict(sql=sqlstring, res=res)])
        dbactionres.save()
        return 'connect fail'
    if not sqlstring.endswith(';'):
        sqlstring = sqlstring + ';'
    ### regx
    sqls =  filter(lambda s: re.match('update|insert|delete', s, flags=re.IGNORECASE), \
                map(lambda x: string.strip(x), sqlstring.split(';'))
            )
    print sqls
    cursor = conn.cursor()
    ### execute sql
    def for_sql_list(sql):
        try:
            cursor.execute(sql)
            rowcount = cursor.rowcount
            if rowcount >= 1:
                return dict(sql=sql, stdout="%s rows affected" % rowcount)
            else:
                return dict(sql=sql, res='0 rows affected')
        except mysql.connector.Error as err:
            return dict(sql=sql, res=str(err))
            sys.exit(1)
    ### regx
    create_sqls =  filter(lambda s: re.match('create', s, flags=re.IGNORECASE), \
                map(lambda x: string.strip(x), sqlstring.split(';'))
            )
    print create_sqls
    ### execute create table
    def for_create_sql(create_sql):
        try:
            cursor.execute(create_sql)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                return dict(sql=create_sql, res='already exists.')
            else:
                return dict(sql=create_sql, res=str(err.msg))
        else:
            return dict(sql=create_sql, stdout='ok')
    ### regx
    skip_sqls =  filter(lambda s: s and not re.match('delete|insert|update|create', s, flags=re.IGNORECASE), \
                map(lambda x: string.strip(x), sqlstring.split(';'))
            )
    res_list = [ dict(sql=sql, res='skip') for sql in skip_sqls if len(skip_sqls) > 0 ] 
    res_list += [ for_create_sql(create_sql) for create_sql in create_sqls if len(create_sqls) > 0 ]
    res_list += [ for_sql_list(sql) for sql in sqls if len(sqls) > 0 ]
    print res_list
    cursor.close()
    conn.close()
    res_dumps = pickle.dumps(res_list)
    dbactionres = DbActionRes.objects.get(pk=id)
    dbactionres.execute_result = pickle.dumps(res_list if len(res_list) else [dict(sql=sqlstring, res='Need  sql')])
    dbactionres.save()



class EmailMsg(object):

    def __init__(self, instance):
        self.context = dict(message=instance)

    def _render(self, filename):
        try:
            return render_to_string(filename, self.context)
        except TemplateDoesNotExist:
            raise Exception('Template %s not found' % filename)

    def get_msg_html(self):
        return self._render('message.html')

    def get_msg_text(self):
        return self._render('message.txt')

    def get_subject_text(self):
        subject_string = self._render('subject.txt').replace('\n', '')
        return subject_string


