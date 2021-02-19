# -*- coding: utf-8 -*-
from django.db import models

class Worker(models.Model):
    workerid = models.CharField('工号', max_length=50L)
    name = models.CharField('姓名', max_length=50L)
    group = models.CharField('部门', max_length=50L)
    location = models.CharField('地区', max_length=50L, default='北京')
    title = models.CharField('职级', max_length=50L, default='初级工程师')
    date = models.DateTimeField('创建日期', auto_now=True)
    class Meta:
        verbose_name_plural = '员工表'
        verbose_name = '员工表'
        db_table = 'gstj_worker'
    def __unicode__(self):
        return self.workerid

class Record(models.Model):
    recordid = models.AutoField('记录号', primary_key=True)
    type = models.CharField('工作类型', max_length=50L)
    taskid = models.CharField('任务号', max_length=50L, blank=True)
    name = models.CharField('提交人', max_length=50L)
    usedtime = models.FloatField('耗时', default=0)
    status = models.CharField('状态', max_length=50L)
    project = models.CharField('所属项目', max_length=50L, blank=True)
    link = models.CharField('文档链接', max_length=500L, blank=True)
    detail = models.CharField('详细描述', max_length=500L, blank=True)
    date = models.DateTimeField('提交日期', auto_now=True)
    class Meta:
        verbose_name_plural = '工时记录'
        verbose_name = '工时记录'
        db_table = 'gstj_record'
    def __unicode__(self):
        return str(self.recordid)+self.name
