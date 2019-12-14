from django import forms
from .models import Comment

class CommentForm(forms.Form):
    
    Name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            
            "placeholder": "Your Name",
            "size" : "30"
        })
    )
    email = forms.EmailField(
        max_length=100,
        widget =forms.EmailInput(attrs={

            "size" : "30",
            "placeholder": "Your Email"

        })
        
    )
    body = forms.CharField(
        max_length=250,
        widget = forms.Textarea(attrs={
            "class": "form-control",
            "placeholder": "Leave a comment!",
            "rows" : "5"
        })
    )
