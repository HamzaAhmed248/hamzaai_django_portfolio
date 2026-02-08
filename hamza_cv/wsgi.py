"""
WSGI config for hamza_cv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamza_cv.settings')

# Get the Django WSGI application
app = get_wsgi_application()

# Wrap with WhiteNoise to serve static files
BASE_DIR = Path(__file__).resolve().parent.parent
static_root = str(BASE_DIR / 'staticfiles')

# Serve static files with WhiteNoise
app = WhiteNoise(
    app,
    root=static_root,
    prefix='static/',
    index_file=True,
    mimetypes={
        '.js': 'application/javascript; charset=utf-8',
        '.css': 'text/css; charset=utf-8',
    }
)

