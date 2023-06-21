from django.shortcuts import render, redirect
from datetime import date
from .forms import CandidateCheckinForm
from .models import Student, Task


def checkin(request):
    context = {}

    # create object of form
    form = CandidateCheckinForm(request.POST or None, request.FILES or None)
    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        student = Student.objects.create(name=request.POST.get("name"), email=request.POST.get("email"))
        student.save()

        tasks = [
            "Initial Email"
            "Resume",
            "Schedule Assessment",
            "Assessment Completed",
            "Assessment Feedback",
            "Schedule Interview",
            "Interview Completed",
            "Interview Feedback"
        ]

        for task in tasks:
            t = Task.objects.create(
                name=task,
                status=Task.INCOMPLETE,
                student=student,
                start_date=date.today(),
                update_date=date.today(),
            )
            t.save()

    context['form'] = form
    return render(request, "recruit/checkin.html", context)
