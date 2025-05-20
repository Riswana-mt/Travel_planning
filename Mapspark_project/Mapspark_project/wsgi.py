"""
WSGI config for Mapspark_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""



import os
import sys
from pathlib import Path

# Calculate paths
BASE_DIR = Path(__file__).resolve().parent.parent
SRC_DIR = BASE_DIR if (BASE_DIR / 'manage.py').exists() else BASE_DIR.parent

# Add to Python path
sys.path.append(str(SRC_DIR))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mapspark_project.settings')

# Initialize application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
