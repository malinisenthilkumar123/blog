from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blogs/', views.post_list, name='post_list'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/create/', views.post_create, name='post_create'),
    path('post/<int:post_id>/update/', views.post_update, name='post_update'),
    path('post/<int:post_id>/delete/', views.post_delete, name='post_delete'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('liked-posts/', views.liked_posts, name='liked_posts'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('blogger/<int:author_id>/', views.blogger_detail, name='blogger_detail'),
    path('bloggers/', views.bloggers_list, name='bloggers_list'),
    path('blog/<int:post_id>/create/', views.create_comment, name='create_comment'),
    path('search/', views.search_results, name='search_results'),
] 