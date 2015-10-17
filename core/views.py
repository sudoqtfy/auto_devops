from django.shortcuts import render
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import views
from django.conf import settings
from .forms import UserForm 
from django.contrib.auth import get_user_model
from django.core.paginator import Paginator, InvalidPage, EmptyPage
import json
from .modals import get_modal_form, UserModal, modal_form, modal_delete
from sysapp.views import (
        _setting_dbserver_data, 
        _setting_product_data,
        _setting_project_data,
        _setting_user_data,
        _setting_version_data)
from dbapp.views import (
        _setting_dbaction_data,
        _setting_dbsearch_data,
        _setting_appaction_data,
        _setting_dbselect_data)
_user = get_user_model()


def login(request, *args, **kwargs):
    if request.method == 'POST' \
            and not request.POST.get('remember', None):
        request.session.set_expiry(0)
    print request.POST
    return views.login(request, *args, **kwargs)


@login_required
def index(request):
    data = {}
    return render(request, 'index.html', data)


#def modal_form(request, form_name="user", id=None, app=None):
#    data =  {'status': True, 'action': 'reload'}
#    template = 'formpage/modal_form.html'
#    data['form'] = create_form(id, request_data=request.POST, form_name='user')
#    if request.method == "POST":
#        template = 'formpage/user_form.html'
#        if data['form'].is_valid():
#            try:
#                instance = u.save()
#                return HttpResponse(json.dumps(data), content_type="application/json")
#            except Exception, e:
#                print str(e)
#    print data['form']
#    data['form_template'] = 'formpage/user_form.html'
#    data['request_path'] = request.path
#    return render(request, template, data)
#    return UserModal(id, form_name).render(request, app)


#def modal_delete(request, form_name="user", id=None, app=None):
#    return UserModal(id, form_name).delete(request)



@login_required
def container_page(request, section):
    data = dict()
    data['section'] = section
    hander_fun = '_setting_%s_data' % section
    if hander_fun in globals():
        data = globals()[hander_fun](request, data)
        paginator = Paginator(data['posts'], settings.PAGE_SIZE)
        cur_page = request.GET.get('page', 1)
        try:
            data['posts'] = paginator.page(cur_page)
        except (EmptyPage, InvalidPage):
            data['posts'] = paginator.page(paginator.num_pages)
    else:
        raise Http404
    query = ''
    for q, r in request.GET.items():
        if q == 'page': continue
        query = query + '&%s=%s' % (q, str(r))
    data['query'] = query
    print data
    return render(request, 'container_page.html', data)

