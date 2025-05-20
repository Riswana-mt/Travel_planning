"""
WSGI config for Mapspark_project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import sys
from pathlib import Path

# Add project directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))



import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Mapspark_project.settings')

application = get_wsgi_application()
