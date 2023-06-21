from django.contrib import admin
from .models import Post, Comment, Images

admin.site.site_header = 'Recruiter'

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Images)