from django.db import models

# Create your models here.

from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    
    class Meta:
        ordering = ['-date_posted']
        
    def __str__(self):
        truncated_content = self.content[:75] + '...' if len(self.content) > 75 else self.content
        return f'Comment by {self.author.username} on {self.post.title}: {truncated_content}'