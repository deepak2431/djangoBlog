from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    email_sent = models.BooleanField()
    received_reply = models.BooleanField()
    assessment_scheduled = models.BooleanField()
    assessment_graded = models.BooleanField()
    schedule_interview = models.BooleanField()

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)
    students = models.ManyToManyField(Student, null=True, blank=True)

    def __str__(self):
        return self.name