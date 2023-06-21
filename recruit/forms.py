from .models import Recruit
import django.forms as forms


# create a ModelForm
class CandidateCheckinForm(forms.Form):
    # specify the name of model to use

    name = forms.CharField(max_length=200)
    email = forms.EmailField(max_length=50)
