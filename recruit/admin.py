from django.contrib import admin
from .models import Student, Event, Task

# Register your models here.
admin.site.register(Student)
admin.site.register(Event)
admin.site.register(Task)