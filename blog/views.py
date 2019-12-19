import json
import urllib
from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from blog.forms import CommentForm, PostForm, ImageForm
from django.views.generic import (View,
    FormView,
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post,Comment, Images
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


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
        images = Images.objects.filter(post=post)
        form = CommentForm()
        context = {
            'post': post,
            'images': images,
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
            images = Images.objects.filter(post=post)
            form = CommentForm()
            context = {
            'post': post,
            'images': images,
            'form': form,
        }          
            return render(request, 'blog/post_detail.html',context)
        form = CommentForm()
        post = get_object_or_404(Post, pk=kwargs['pk'])   
        images = Images.objects.filter(post=post)
        context = {
            'post': post,
            'images': images,
            'form': form
        }          
        return render(request, 'blog/post_detail.html', context)



@login_required(login_url='login')
def createPost(request):
    #creating a set of forms for multiple images
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=6)

    #if request is POST, validate and save both the forms
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if postForm.is_valid() and formset.is_valid():
            new_post = Post()
            new_post.title = postForm.cleaned_data['title']
            new_post.content = postForm.cleaned_data['content']
            new_post.topic = postForm.cleaned_data['topic']
            new_post.author = request.user
            new_post.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(post=new_post, image=image)
                    photo.save()
            messages.success(request, "Posted!")
            return HttpResponseRedirect("/")
        else:
            print(postForm.errors, formset.errors)
    # if request is GET, display empty forms
    else:
        postForm = PostForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    
    context = {'postForm': postForm, 'formset': formset}
    return render(request, 'blog/post_form.html', context)

@login_required(login_url='login')
def updatePost(request,pk):
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=2)
    post = get_object_or_404(Post, pk=pk)
    old_images = Images.objects.filter(post=post)

    #check authorization of user
    if post.author != request.user:
        messages.success(request, "You are not authorized to update this post!")
        return HttpResponseRedirect("/")

    #if request is POST, update both the forms    
    if request.method == 'POST':
        postForm = PostForm(request.POST)
        formset = ImageFormSet(request.POST,request.FILES, queryset=Images.objects.none())
        if postForm.is_valid() and formset.is_valid() :
            post.title = postForm.cleaned_data['title']
            post.content = postForm.cleaned_data['content']
            post.topic = postForm.cleaned_data['topic']
            post.save()
            old_images.delete()
            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(post=post, image=image)
                    photo.save()
            messages.success(request, "Post Updated!")
            return HttpResponseRedirect("/")
        else:
            messages.success(request, "Post Not Updated! Upload all Images")
            return HttpResponseRedirect("/")
            
    #if request is GET, return both the forms with Initial values        
    else:
        postForm = PostForm(instance=post)
        formset = ImageFormSet(queryset=Images.objects.filter(post=post))
    
    context = {'postForm': postForm, 'formset': formset}
    return render(request,'blog/post_form.html', context)


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



