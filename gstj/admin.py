from django.contrib import admin
from .models import Worker,Record,Projects
class WorkerAdmin(admin.ModelAdmin):
    list_filter = ('group', 'location', 'title', 'date')
    list_display = ('workerid', 'name', 'group', 'location', 'title', 'date')
    ordering = ('-date',)
class RecordAdmin(admin.ModelAdmin):
    list_filter = ('type', 'name', 'status', 'project')
    list_display = ('type', 'name', 'taskid', 'status', 'project', 'usedtime', 'date')
    ordering = ('-date',)

admin.site.register(Worker, WorkerAdmin)
admin.site.register(Record, RecordAdmin)
admin.site.register(Projects)
