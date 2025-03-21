from django.contrib import admin
from .models import Post, Comment

# Inline model for displaying comments with posts
class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0  # No extra empty forms
    readonly_fields = ('date_posted',)
    fields = ('author', 'content', 'date_posted')
    can_delete = True
    show_change_link = True

# Register your models here.
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'date_posted', 'comment_count')
    list_filter = ('author', 'date_posted')
    search_fields = ('title', 'content')
    date_hierarchy = 'date_posted'
    inlines = [CommentInline]
    
    def comment_count(self, obj):
        return obj.comments.count()
    comment_count.short_description = 'Comments'

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('truncated_content', 'post', 'author', 'date_posted')
    list_filter = ('author', 'date_posted')
    search_fields = ('content',)
    date_hierarchy = 'date_posted'
    
    def truncated_content(self, obj):
        if len(obj.content) > 75:
            return obj.content[:75] + '...'
        return obj.content
    truncated_content.short_description = 'Comment'
