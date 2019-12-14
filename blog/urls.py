from django.urls import path
from .views import (PostListView,
                    # CreateCommentView,
                    PostDeleteView,
                    PostDetailView,
                    PostCreateView,
                     PostUpdateView,
                     UserPostListView)
from .import views

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>/', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    #  path('post/<int:pk>/comment',CreateCommentView.as_view(), name='create-comment'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('about/', views.about, name='blog-about'),
]