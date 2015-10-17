#!-*- coding: utf8 -*-
from django import template
from django.contrib.auth import get_user_model
from dbapp.models import  DbActionRes
import json
import string
try:
    import cPickle as pickle
except ImportErro:
    import pickle

_user = get_user_model()

register = template.Library()

sys_section_pattern = [
        'user',
        'project',
        'version',
        'product',
        'dbserver',
]

db_section_pattern = [
        'dbaction',
        'dbsearch',
        'appaction',
        'dbselect',
]

@register.simple_tag
def sys_block_func(section):
    if section in sys_section_pattern: return 'style="display:block"'


@register.simple_tag
def db_block_func(section):
    if section in db_section_pattern: return 'style="display:block"'

@register.simple_tag
def active_func(section):
    return 'class="active"'


@register.simple_tag
def dbaction_result(instance):
    dbactionres = DbActionRes.objects.get(dbaction=instance)
    return dbactionres['execute_status']


@register.simple_tag
def dbaction_sql_display(sqlstring):
    sqlstring = str(sqlstring).strip()
    li_html = '''<li class="text-primary">{0}</li>'''
    sql_html = ''
    if not sqlstring.endswith(';'): sqlstring += ';'
    sqllist = filter(lambda x: x,map(lambda s: string.strip(s), sqlstring.split(';')))
    for sql in sqllist:
        sql_html += li_html.format(sql)
    return sql_html



@register.simple_tag
def dbaction_result_display(dstring):
    dstring = str(dstring).strip()
    if not dstring:
        return  """
                <div class="alert alert-danger">
                    <button type="button" class="close" data-dismiss="alert">
                        <i class="icon-remove"></i>
                    </button>

                    <strong>
                        <i class="icon-remove"></i>
                        Oh snap!
                    </strong>
                    没有查到执行结果 可能还未执行完
                    <br>
                </div>
                """

    ddict = pickle.loads(dstring)
    result_html = ''
    ok_html = '''
                <li class="text-success">
                    <i class="icon-ok bigger-110 green"></i>
                    {0}
                </li>
                <div class="alert alert-block alert-success">
                        <button type="button" class="close" data-dismiss="alert">
                            <i class="icon-remove"></i>
                        </button>
                        <strong class="green">
                        <i class="icon-ok green"></i>
                            INFO
                        </strong>
                        {1}
                 </div>
              '''
    fail_html = '''
                    <li class="text-danger">
                    <i class="icon-remove bigger-110 red"></i>
                    {0}
                    </li>
                        <div class="alert alert-danger">
                            <button type="button" class="close" data-dismiss="alert">
                                <i class="icon-remove"></i>
                            </button>
                            <strong>
                                <i class="icon-remove"></i>
                                Error!
                            </strong>
                            {1}
                            <br>
                        </div>
               '''
    other_html = '''
                <li class="text-success">
                    <i class="icon-ok bigger-110 green"></i>
                    {0}
                </li>
              '''
    for res_dict in ddict:
        if 'stdout' in res_dict:
            result_html += ok_html.format(res_dict.get('sql'), res_dict.get('stdout', 'No Tip'))
        elif "res" in res_dict:
            result_html += fail_html.format(res_dict.get('sql'), res_dict.get('res'))
        else:
            result_html += other_html.format(res_dict.get('sql', ''))
    return result_html
        

@register.simple_tag
def message_html_display(dstring, html=True):
    dstring = str(dstring).strip()
    if not dstring: 'No Result'
    if not html:
        if dstring.endswith(';'): dstring += ';'
        result_text = ''
        print dstring.split(';')
        for index, sql in enumerate(filter(lambda s: s,dstring.split(';'))):
            result_text += '%s. %s\n' % (index+1, sql)
        return result_text

    ddict = pickle.loads(dstring)
    result_html = ''
    ok_html = '''
                    <li style="color:green"><span>√&nbsp;&nbsp;</span>{0}</li>
              '''
    fail_html = '''
                    <li><del style="color:red">{0}</del>[{1}]</li>
               '''
    for res_dict in ddict:
        if 'res' not in res_dict:
            result_html += ok_html.format(res_dict.get('sql'))
        else:
            result_html += fail_html.format(res_dict.get('sql'), res_dict.get('res'))
    return result_html


@register.simple_tag
def message_text_display(dstring, res=True):
    dstring = str(dstring).strip()
    if not dstring: 'No Result'
    result_text = ''
    if not res:
        if dstring.endswith(';'): dstring += ';'
        for index, sql in enumerate(filter(lambda s: s,dstring.split(';'))):
            result_text += '%s. %s\n' % (index+1, sql)
        return result_text

    ddict = pickle.loads(dstring)
    ok_text = '''
                    {0}\n
              '''
    fail_text = '''
                    {0}[{1}]\n
               '''
    for res_dict in ddict:
        if 'res' not in res_dict:
            result_text += ok_text.format(res_dict.get('sql'))
        else:
            result_text += fail_text.format(res_dict.get('sql'), res_dict.get('res'))
    return result_text
