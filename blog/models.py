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
    like = models.ManyToManyField(User, related_name='likes', blank='True')

    save = models.ManyToManyField(User, related_name='saves', blank='True')

    viewed_users = models.ManyToManyField(User, related_name="viewed_users")

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    isQuestion = models.BooleanField(default=False)

    def __str__(self):
        return self.title
        
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})
    
    def total_likes(self):
        return self.like.count()

class Comment(models.Model):

    Name = models.CharField(max_length=60)
    body = models.TextField()
    email = models.EmailField(max_length = 50,default="")
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self',on_delete=models.CASCADE,null =True,related_name = 'replies')
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    # def get_absolute_url(self):
    #     return reverse('post-detail', kwargs={'pk': Post.pk})



class Images(models.Model):
    post = models.ForeignKey(Post, default=None, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post_images/',verbose_name='Image')



class Answer(models.Model):
    question = models.ForeignKey('Post',on_delete=models.CASCADE)
    answer = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)