from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comment
from django.contrib.auth.models import User
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CommentForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def home(request):
    """
    Home page view that displays an index page describing the site.
    """
    return render(request, 'blog/home.html', {
        'title': 'DIY Django Mini Blog',
        'welcome_message': 'Welcome to the DIY Django Mini Blog!'
    })

def post_list(request):
    """
    View to display a list of all blog posts.
    - Sorted by post date (newest to oldest)
    - Paginated in groups of 5 articles
    """
    posts = Post.objects.all().order_by('-date_posted')
    
    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'title': 'All Blog Posts',
        'page_obj': page_obj,
    })

def post_detail(request, post_id):
    """
    View to display a single blog post.
    """
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    
    return render(request, 'blog/post_detail.html', {
        'title': post.title,
        'post': post,
        'comments': comments,
    })

def author_detail(request, author_id):
    """
    View to display details about a blog author and their posts.
    """
    author = get_object_or_404(User, id=author_id)
    posts = Post.objects.filter(author=author).order_by('-date_posted')
    
    # Pagination
    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/author_detail.html', {
        'title': f'Posts by {author.username}',
        'author': author,
        'page_obj': page_obj,
    })

def blogger_detail(request, author_id):
    """
    View to display blogger information and a list of their posts without pagination.
    - Sorted by post date (newest to oldest)
    - Not paginated
    - List items display just the blog post name and post date
    """
    author = get_object_or_404(User, id=author_id)
    posts = Post.objects.filter(author=author).order_by('-date_posted')
    
    return render(request, 'blog/blogger_detail.html', {
        'title': f'Blogger: {author.username}',
        'author': author,
        'posts': posts,
    })

def bloggers_list(request):
    """
    View to display a list of all bloggers on the system.
    """
    # Get all users who have at least one post, annotated with post count
    bloggers = User.objects.annotate(post_count=Count('post')).filter(post_count__gt=0).order_by('username')
    
    return render(request, 'blog/bloggers_list.html', {
        'title': 'All Bloggers',
        'bloggers': bloggers,
    })

@login_required
def create_comment(request, post_id):
    """
    View to create a comment for a blog post.
    - Accessible only to logged-in users
    - Redirects back to the blog post after comment is created
    """
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Your comment has been added!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = CommentForm()
    
    return render(request, 'blog/create_comment.html', {
        'title': f'Comment on {post.title}',
        'form': form,
        'post': post,
    })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
