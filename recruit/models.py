from django.db import models


class Student(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=50, unique=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    email_sent = models.BooleanField(default=False)
    received_reply = models.BooleanField(default=False)
    assessment_scheduled = models.BooleanField(default=False)
    assessment_graded = models.BooleanField(default=False)
    schedule_interview = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField()
    notes = models.CharField(max_length=200, blank=True, null=True)
    students = models.ManyToManyField(Student, null=True, blank=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    INCOMPLETE = 'INCOMPLETE'
    IN_PROGRESS = 'IN_PROGRESS'
    COMPLETED = 'COMPLETED'
    STATUS_CHOICES = [
        (INCOMPLETE, 'Incomplete'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed')
    ]
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default=INCOMPLETE
    )
    start_date = models.DateField()
    update_date = models.DateField()
    student = models.ForeignKey(Student, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def is_completed(self):
        return self.status == self.COMPLETED
