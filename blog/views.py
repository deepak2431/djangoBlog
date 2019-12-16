import json
import urllib
from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from blog.forms import CommentForm
from django.views.generic import (View,
    FormView,
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post,Comment

def about(request):
    return render (request,'blog/about.html', {'title':'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_post.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(View):

    # when clicked on the title of post get function is trigeered 
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(Post, pk=kwargs['pk'])
        form = CommentForm()
        context = {
            'post': post,
            'form': form
        }
        return render(request, 'blog/post_detail.html', context)
    
    # when commented post request is forwarded on this view and post function is triggered
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        if form.is_valid():
            
            post = get_object_or_404(Post, pk=kwargs['pk'])
            
                
            post.comment_set.create(
                Name = form.cleaned_data['Name'],
                email = form.cleaned_data['email'],
                body = form.cleaned_data['body']
            )
               
            form = CommentForm()
            context = {
            'post': post,
            'form': form,
        }          
            return render(request, 'blog/post_detail.html',context)
        form = CommentForm()
        post = get_object_or_404(Post, pk=kwargs['pk'])   
        context = {
            'post': post,
            'form': form
        }          
        return render(request, 'blog/post_detail.html', context)



class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','topic','content']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

class PostUpdateView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content']
    template_name = 'blog/post_form.html'


    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False

class PostDeleteView(LoginRequiredMixin,UserPassesTestMixin,DeleteView):
    model = Post
    template_name = 'blog/post_delete_confirm.html'
    success_url = '/'


    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        else:
            return False



