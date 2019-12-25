from django import forms
from django.forms import Textarea
from .models import Comment, Post, Images, Answer

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


class PostForm(forms.ModelForm):
    TOPICS = [('NONE','None'),('TECHNOLOGY','Technology'),('CULTURE','Culture'),('ENTERTAINMENT','Entertainment'),('MUSIC','Music'),('DANCE','Dance')]
    title = forms.CharField(max_length=100)
    content = forms.CharField(widget=forms.Textarea)
    topic = forms.CharField(max_length=50,widget=forms.Select(choices=TOPICS))
    class Meta:
        model = Post
        fields = ('title', 'topic', 'content')   


class ImageForm(forms.ModelForm):
    image = forms.ImageField(label='Image')    
    class Meta:
        model = Images
        fields = ('image', )


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'topic', 'content')   
        labels = {
            'content':'Question'
        }
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = {'answer'}
        widgets = {
            'answer':Textarea(attrs={'placeholder':"Type your answer here",'rows':5}),
        }