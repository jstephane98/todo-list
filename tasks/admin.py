from django.contrib import admin

from tasks.models import Task, Collection

# Register your models here.
admin.site.register(Task)
admin.site.register(Collection)
