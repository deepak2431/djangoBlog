from django.urls import path
from .views import (PostListView,
                    PostDeleteView,
                    PostDetailView,
                     UserPostListView,
                     LikepostView)
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', views.createPost, name='post-create'),
    path('post/<int:pk>/update/', views.updatePost, name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
    path('post/<int:pk>/like/',LikepostView.as_view() ,name='post-like'),
]