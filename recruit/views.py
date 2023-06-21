from django.shortcuts import render, redirect
from .forms import CandidateCheckinForm
from .models import Student


def checkin(request):
    context = {}

    # create object of form
    form = CandidateCheckinForm(request.POST or None, request.FILES or None)

    # check if form data is valid
    if form.is_valid():
        # save the form data to model
        student = Student.objects.create(name=request.POST.get("name"), email=request.POST.get("email"))
        student.save()

    context['form'] = form
    return render(request, "recruit/checkin.html", context)
