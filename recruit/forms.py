from .models import Student
from django.forms import ModelForm


# create a ModelForm
class CandidateCheckinForm(ModelForm):
    # specify the name of model to use
    class Meta:
        model = Student
        fields = ["name", "email"]
