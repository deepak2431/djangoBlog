import json
import urllib
from django.db.models import Q
from django.conf import settings
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.contrib import messages
from blog.forms import CommentForm, PostForm, ImageForm, QuestionForm, AnswerForm
from django.views.generic import (View,
    FormView,
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView)
from .models import Post,Comment,Images,Answer
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import modelformset_factory


def about(request):
    return render (request,'blog/about.html', {'title':'About'})

class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 5
    def get_queryset(self):
        if(self.kwargs.get('url') == 'question_form'):
            post_set = Post.objects.filter(isQuestion = True)
        elif(self.kwargs.get('url') == None):
            post_set = Post.objects.filter(isQuestion = False)
        query = self.request.GET.get('query')
        if query:
            return post_set.filter(Q(title__icontains = query) | Q(topic__icontains = query)).order_by('-date_posted')
        else:
            return post_set.order_by('-date_posted')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Q_Form'] = False
        if(self.kwargs.get('url') == 'question_form'):
            context['Q_Form'] = True
        return context         

class PostmarkedView(ListView):
    model = Post
    template_name = 'blog/bookmark.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(isQuestion = False, save = self.request.user.id) 

        return context


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
        is_liked = False
        is_saved = False
        if post.save.filter(id=request.user.id).exists():
            is_saved = True
        if post.like.filter(id=request.user.id).exists():
            is_liked = True
        images = Images.objects.filter(post=post)
        form = CommentForm()
        comments = Comment.objects.filter(post = post,reply = None).order_by('-id')
        if request.user.is_authenticated and request.user != post.author:
            post.viewed_users.add(request.user)
        context = {
            'post'      : post,
            'form'      : form,
            'comments'  : comments,
            'images'    : images,
            'is_liked'  : is_liked,
            'is_saved'  : is_saved,
            'total_likes': post.total_likes()
        }
        return render(request,'blog/post_detail.html', context)
    
    # when commented post request is forwarded on this view and post function is triggered
    def post(self, request, *args, **kwargs):
        form = CommentForm(request.POST or None)
        if form.is_valid():
            
            post = get_object_or_404(Post, pk=kwargs['pk'])
            is_saved = False
            if post.save.filter(id=request.user.id).exists():
                is_saved = True
            is_liked = False
            if post.like.filter(id=request.user.id).exists():
                is_liked = True
            reply_id = request.POST.get('comment_id')
            comment_parent = None
            if reply_id:
                comment_parent = Comment.objects.get(id=reply_id)
                
            post.comment_set.create(
                Name = form.cleaned_data['Name'],
                email = form.cleaned_data['email'],
                body = form.cleaned_data['body'],
                reply = comment_parent
            )

            messages.success(request, 'Comment successful')  
            images = Images.objects.filter(post=post)
            form = CommentForm()
            comments = Comment.objects.filter(post = post,reply = None).order_by('-id')
            context = {
            'post'      : post,
            'images'    : images,
            'form'      : form,
            'comments'  : comments,
            'is_liked'  : is_liked,
            'is_saved'  : is_saved,
            'total_likes': post.total_likes()
            }          
            return render(request, 'blog/post_detail.html',context)
        form = CommentForm()
        post = get_object_or_404(Post, pk=kwargs['pk'])
        is_saved = False
        if post.save.filter(id=request.user.id).exists():
            is_saved = True   
        is_liked = False
        if post.like.filter(id=request.user.id).exists():
            is_liked = True

        messages.warning(request, 'Some error occured')
        comments = Comment.objects.filter(post = post,reply = None).order_by('-id')
        images = Images.objects.filter(post=post)
        

        
        context = {
            'post'      : post,
            'images'    : images,
            'form'      : form,
            'comments'  : comments,
            'is_liked'  : is_liked,
            'is_saved'  : is_saved,
            'total_likes': post.total_likes()
        }          
        return render(request, 'blog/post_detail.html', context)



class LikepostView(LoginRequiredMixin ,View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
   
    
    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_like'))
        is_liked = False
        if post.like.filter(id=request.user.id).exists():
            post.like.remove(request.user)
            is_liked = False
        else:
            post.like.add(request.user)
            is_liked = True
        return HttpResponseRedirect(post.get_absolute_url())

class SavepostView(LoginRequiredMixin ,View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(Post, id=request.POST.get('post_save'))
        is_saved = False
        if post.save.filter(id=request.user.id).exists():
            post.save.remove(request.user)
            is_saved = False
        else:
            post.save.add(request.user)
            is_saved = True
        return HttpResponseRedirect(post.get_absolute_url())    

@login_required(login_url='login')
def askQuestion(request):
    #creating a set of forms for multiple images
    ImageFormSet = modelformset_factory(Images, form=ImageForm, extra=6)

    #if request is POST, validate and save both the forms
    if request.method == 'POST':
        questionForm = QuestionForm(request.POST)
        formset = ImageFormSet(request.POST, request.FILES, queryset=Images.objects.none())

        if questionForm.is_valid() and formset.is_valid():
            new_question = Post()
            new_question.title = questionForm.cleaned_data['title']
            new_question.content = questionForm.cleaned_data['content']
            new_question.topic = questionForm.cleaned_data['topic']
            new_question.author = request.user
            new_question.isQuestion = True
            new_question.save()

            for form in formset.cleaned_data:
                if form:
                    image = form['image']
                    photo = Images(post=new_post, image=image)
                    photo.save()
            messages.success(request, "Posted!")
            return HttpResponseRedirect("/questions/form/")
        else:
            print(questionForm.errors, formset.errors)
    # if request is GET, display empty forms
    else:
        questionForm = QuestionForm()
        formset = ImageFormSet(queryset=Images.objects.none())
    
    context = {'postForm': questionForm, 'formset': formset, 'Q_Form':True}
    return render(request, 'blog/post_form.html', context)



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

class AnswersListView(ListView):
    model = Answer
    context_object_name = 'answers'
    template_name = 'blog/answers.html'
    paginate_by = 2
    
    def get(self, request, *args, **kwargs):
        form = AnswerForm()
        question = get_object_or_404(Post, pk=kwargs['pk'])
        images = Images.objects.filter(post=question)
        context = {
            'answers' : Answer.objects.filter(question=question).order_by('-date_posted'),
            'question' : question,
            'images' :images,
            'answer_form':form
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = AnswerForm(request.POST or None)
        question = get_object_or_404(Post, pk=kwargs['pk'])
        images = Images.objects.filter(post=question)
        if form.is_valid():
            newAnswer = Answer()
            newAnswer.question = question
            newAnswer.author = request.user
            newAnswer.answer = form.cleaned_data['answer']
            newAnswer.save()
            context = {
                'answers' : Answer.objects.filter(question=question).order_by('-date_posted'),
                'question' : question,
                'images' :images,
                'answer_form':AnswerForm()
            }
            return render(request,self.template_name,context)
        form = AnswerForm()
        question = get_object_or_404(Post, pk=kwargs['pk'])
        images = Images.objects.filter(post=question)
        context = {
            'answers' : Answer.objects.filter(question=question).order_by('-date_posted'),
            'question' : question,
            'images' :images,
            'answer_form':form
        }
        return render(request, self.template_name, context)