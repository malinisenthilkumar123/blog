from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('blogger/<int:author_id>/', views.blogger_detail, name='blogger_detail'),
    path('bloggers/', views.bloggers_list, name='bloggers_list'),
    path('blog/<int:post_id>/create/', views.create_comment, name='create_comment'),
] 