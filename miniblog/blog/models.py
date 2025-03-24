from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category, related_name='posts', blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    def __str__(self):
        return self.title
    
    def total_likes(self):
        return self.likes.count()
    
    class Meta:
        ordering = ['-date_posted']

class Comment(models.Model):
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.post.title}'
    
    class Meta:
        ordering = ['-date_posted']