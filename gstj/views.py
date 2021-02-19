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
 
def index(request):
    typelist = ('bug','开发','调研','学习分享','文档','沟通支持','其它')
    statuslist = ('进行中','完成','自修提交','转出','关闭','其它')
    workerlist = Worker.objects.all()
    context = { 'typelist':typelist, 'statuslist':statuslist, 'workerlist':workerlist }
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
    group = request.GET.get('group')
    year = request.GET.get('year')
    month = request.GET.get('month')
    if not group or group == 'all':
        workers = Worker.objects.all()
        ret = Record.objects.all()
        group = '全体'
    else:
        workers = Worker.objects.filter(group=group)
        ret = Record.objects.filter(name__in=workers.values_list('name', flat=True))
    if not year or not month:
        year = datetime.datetime.now().year
        month = datetime.datetime.now().month
    ret = ret.filter(date__year=year, date__month=month)
    #if perpage and pageno:
    #    ret = ret[int(perpage)*int(pageno)-int(perpage):int(perpage)*int(pageno)]
    groups = Worker.objects.values_list('group', flat=True).distinct()
    sum = []
    for worker in workers:
        hours = 0
        tasks = 0
        for r in ret.filter(name=worker.name):
           hours += r.usedtime
           tasks += 1
        sum.append({'location':worker.location, 'group':worker.group, 'workerid':worker.workerid, 'name':worker.name, 'title':worker.title, 'hours':hours, 'tasks':tasks})
    context = { 'ret':ret, 'groups':groups, 'year':year, 'month':month, 'group':group, 'sum':sum }
    return render(request, "stat.html", context)
