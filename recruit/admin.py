from django.contrib import admin
from .models import Student, Event, Task, Position


class TaskInline(admin.TabularInline):
    model = Task
    extra = 0


class EventStudentsInline(admin.TabularInline):
    model = Event.students.through
    extra = 0


class EventPositionsInline(admin.TabularInline):
    model = Event.positions.through
    extra = 0


class StudentAdmin(admin.ModelAdmin):
    inlines = [
        EventStudentsInline,
        TaskInline
    ]
    exclude = (
        "email_sent",
        "received_reply",
        "assessment_scheduled",
        "assessment_graded",
        "schedule_interview",
    )


class EventAdmin(admin.ModelAdmin):
    inlines = [
        EventPositionsInline,
        EventStudentsInline,
    ]
    exclude = ("positions", "students",)


# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Position)
