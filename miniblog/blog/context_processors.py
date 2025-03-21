from django.contrib.auth.models import User
from django.db.models import Count

def bloggers_processor(request):
    """
    Context processor that adds the list of bloggers to all templates.
    """
    # Get users who have at least one post, annotated with their post count
    bloggers = User.objects.annotate(post_count=Count('post')).filter(post_count__gt=0).order_by('username')
    
    return {
        'bloggers': bloggers,
    } 