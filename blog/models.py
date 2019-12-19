from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
    TOPICS = [('TECHNOLOGY','Technology'),('CULTURE','Culture'),('ENTERTAINMENT','Entertainment'),('MUSIC','Music'),('DANCE','Dance'),('NONE','None')]
    title = models.CharField(max_length=100)
    topic = models.CharField(max_length=50,blank = False,default=('NONE','None'),choices=TOPICS)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})

class Comment(models.Model):

    Name = models.CharField(max_length=60)
    body = models.TextField()
    email = models.EmailField(max_length = 50,default="")
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': Post.pk})



class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/',verbose_name='Image')





