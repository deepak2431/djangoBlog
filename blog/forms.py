from django import forms
from .models import Comment

class CommentForm(forms.Form):
    
    Name = forms.CharField(
        max_length=60,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Your Name",
            
        })
    )
    email = forms.EmailField(max_length=50)
    body = forms.CharField(
        max_length=250,
        widget = forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!"
        })
    )
