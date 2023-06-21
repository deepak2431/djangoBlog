from django.contrib import admin
from .models import Student, Event, Task


class TaskInline(admin.TabularInline):
    model = Task


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        TaskInline
    ]


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Event)
