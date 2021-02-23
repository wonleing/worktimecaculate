# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
#from django.utils.encoding import smart_str
#from django.db.models import Q
#from django.core import serializers
#import xml.etree.ElementTree as ET
import datetime
from gstj.models import *
workdays = (20, 17, 23, 22, 19, 21, 22, 22, 22, 17, 22, 23)
typelist = ('bug','开发','调研','学习分享','文档','沟通支持','其它')
statuslist = ('进行中','完成','自修提交','转出','关闭','其它')

@csrf_exempt
def dologin(request):
    ac = request.POST.get('account')
    pw = str(request.POST.get('password'))
    try:
        request.session['login_user'] = Worker.objects.get(workerid=ac, password=pw)
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../"></head>登录成功</html>''')
    except:
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head>密码错误</html>''')

def logout(request):
    request.session['login_user'] = ""
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head>登出成功!</html>''')

@csrf_exempt
def changepwd(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return HttpResponse('请先登录')
    elif not request.POST.get('newpwd') == request.POST.get('againpwd'):
        return HttpResponse('两次密码不一致')
    else:
        try:
            ret = Worker.objects.get(workerid=request.session['login_user'].workerid)
            ret.password = request.POST.get('newpwd')
            ret.save()
            return HttpResponse('密码修改成功')
        except:
            HttpResponse('登录身份过期，请重新登录')
 
def index(request):
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    year = datetime.datetime.now().year
    month = datetime.datetime.now().month
    projectlist = Projects.objects.all().values_list('project', flat=True)
    recorded = 0
    if request.session['login_user']:
        for ret in Record.objects.filter(name=request.session['login_user'].name, date__year=year, date__month=month):
            recorded += ret.usedtime
    suppose = workdays[month-1] * 8
    context = { 'login_user': request.session['login_user'], 'typelist':typelist, 'statuslist':statuslist, 'projectlist':projectlist, 'recorded':recorded, 'suppose':suppose }
    return render(request, "index.html", context)

def doinput(request):
    type = request.POST.get('type')
    name = request.POST.get('name')
    status = request.POST.get('status')
    taskid = request.POST.get('taskid')
    usedtime = request.POST.get('usedtime')
    project = request.POST.get('project')
    link = request.POST.get('link')
    detail = request.POST.get('detail')
    Record(type=type, name=name, status=status, taskid=taskid, usedtime=float(usedtime), project=project, link=link, detail=detail).save()
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head><h1>提交完成</h1></html>''')

def stat(request):
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    group = request.GET.get('group')
    year = request.GET.get('year')
    month = request.GET.get('month')
    project = request.GET.get('project')
    if group:
        workers = Worker.objects.filter(group=group)
        ret = Record.objects.filter(name__in=workers.values_list('name', flat=True))
    else:
        workers = Worker.objects.all()
        ret = Record.objects.all()
        group = u'全体'
    if project: 
        ret = ret.filter(project=project)
    else:
        project = u'全部'
    if not year or not month:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    ret = ret.filter(date__year=year, date__month=month)
    #if perpage and pageno:
    #    ret = ret[int(perpage)*int(pageno)-int(perpage):int(perpage)*int(pageno)]
    groups = Worker.objects.values_list('group', flat=True).distinct()
    projects = Projects.objects.values_list('project', flat=True).distinct()
    sum = []
    totalhour = 0
    totaltask = 0
    for worker in workers:
        hours = 0
        tasks = 0
        for r in ret.filter(name=worker.name):
           hours += r.usedtime
           tasks += 1
        totalhour += hours
        totaltask += tasks
        sum.append({'location':worker.location, 'group':worker.group, 'workerid':worker.workerid, 'name':worker.name, 'title':worker.title, 'hours':hours, 'tasks':tasks})
    context = { 'login_user': request.session['login_user'], 'ret':ret, 'groups':groups, 'projects':projects, 'year':year, 'month':month, 'group':group, 'project':project, 'sum':sum, 'totalhour':totalhour, 'totaltask':totaltask }
    return render(request, "stat.html", context)
