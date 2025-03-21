"""
URL configuration for myproject project.
This file imports and includes the URL patterns from miniblog project.
"""
from django.urls import path, include

# Import URLconf from miniblog
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'miniblog')))
from miniblog.urls import urlpatterns

# You can add additional URL patterns here if needed
# urlpatterns += [
#     path('additional/', view_function),
# ] 