from django.urls import path
from .views import (PostListView,
                    PostDeleteView,
                    PostDetailView,
                     UserPostListView,
                     LikepostView,
                     PostmarkedView,
                     SavepostView)
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('questions/form/', PostListView.as_view(), name='question-home', kwargs={'url':'question_form'}),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('question/new/', views.askQuestion, name='question-ask'),
    path('answers/post/<int:pk>',views.AnswersListView.as_view(), name='answers-list'),
    path('post/new/', views.createPost, name='post-create'),
    path('post/<int:pk>/update/', views.updatePost, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('bookmarks/',PostmarkedView.as_view() , name='blog-save'),
    path('post/<int:pk>/like/',LikepostView.as_view() ,name='post-like'),
    path('post/<int:pk>/save/',SavepostView.as_view() ,name='post-save'),
]