from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Post, Comment
from django.contrib.auth.models import User
from django.db.models import Count, Q
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from .forms import CommentForm, UserRegisterForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def home(request):
    """
    Home page view that displays an index page describing the site.
    """
    context = {
        'title': 'DIY Django Mini Blog',
        'welcome_message': 'Welcome to the DIY Django Mini Blog!',
        'bloggers': User.objects.filter(post__isnull=False).distinct()
    }
    
    # Add liked posts for authenticated users
    if request.user.is_authenticated:
        context['liked_posts'] = Post.objects.filter(likes=request.user).order_by('-date_posted')[:3]
    
    return render(request, 'blog/home.html', context)

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
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def post_create(request):
    """
    View to create a new blog post.
    - Accessible only to logged-in users
    - Redirects to the new blog post after creation
    """
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            post = Post.objects.create(
                title=title, 
                content=content, 
                author=request.user
            )
            messages.success(request, 'Your post has been created!')
            return redirect('post_detail', post_id=post.id)
    
    return render(request, 'blog/post_create.html', {
        'title': 'Create New Post',
    })

@login_required
def post_update(request, post_id):
    """
    View to update an existing blog post.
    - Only the post author can edit their own post
    - Accessible only to logged-in users
    - Redirects to the updated blog post after completion
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author of the post
    if post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        
        if title and content:
            post.title = title
            post.content = content
            post.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post_detail', post_id=post.id)
    
    return render(request, 'blog/post_update.html', {
        'title': 'Edit Post',
        'post': post,
    })

@login_required
def post_delete(request, post_id):
    """
    View to delete an existing blog post.
    - Only the post author can delete their own post
    - Accessible only to logged-in users
    - Redirects to the blog list after deletion
    - Requires confirmation
    """
    post = get_object_or_404(Post, id=post_id)
    
    # Check if user is the author of the post
    if post.author != request.user:
        messages.error(request, "You don't have permission to delete this post.")
        return redirect('post_detail', post_id=post.id)
    
    if request.method == 'POST':
        post_title = post.title
        post.delete()
        messages.success(request, f'Your post "{post_title}" has been deleted.')
        return redirect('post_list')
    
    return render(request, 'blog/post_delete.html', {
        'title': 'Delete Post',
        'post': post,
    })

@csrf_exempt
@login_required
def like_post(request, post_id):
    """
    View to handle liking/unliking a post
    - Only authenticated users can like posts
    - Returns JSON response for AJAX requests or redirects for standard requests
    """
    try:
        post = get_object_or_404(Post, id=post_id)
        user = request.user
        
        # Toggle like status
        if user in post.likes.all():
            # User already liked the post, so unlike it
            post.likes.remove(user)
            liked = False
        else:
            # User hasn't liked the post, so like it
            post.likes.add(user)
            liked = True
        
        # Check if it's an AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Return JSON response for AJAX requests
            return JsonResponse({
                'liked': liked,
                'likes_count': post.total_likes()
            })
        else:
            # Redirect back to the referring page for standard requests
            referer = request.META.get('HTTP_REFERER')
            if referer:
                return redirect(referer)
            else:
                return redirect('post_detail', post_id=post_id)
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': str(e)}, status=500)
        else:
            return redirect('post_detail', post_id=post_id)

@login_required
def liked_posts(request):
    """
    View to display all posts liked by the current user
    """
    posts = Post.objects.filter(likes=request.user).order_by('-date_posted')
    
    return render(request, 'blog/liked_posts.html', {
        'title': 'Posts You Like',
        'posts': posts,
        'bloggers': User.objects.filter(post__isnull=False).distinct()
    })

def search_results(request):
    """
    View to display search results.
    - Searches in post title and content
    - Returns all matching posts
    """
    query = request.GET.get('q', '')
    
    if query:
        # Search in title and content using Q objects for OR condition
        search_results = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-date_posted')
    else:
        search_results = Post.objects.none()
    
    # Get bloggers for sidebar
    bloggers = User.objects.filter(post__isnull=False).distinct()
    
    context = {
        'title': 'Search Results',
        'query': query,
        'search_results': search_results,
        'bloggers': bloggers,
    }
    
    return render(request, 'blog/search_results.html', context)
