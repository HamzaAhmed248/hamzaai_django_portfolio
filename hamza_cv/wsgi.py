"""
WSGI config for hamza_cv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os
import sys
from pathlib import Path

from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamza_cv.settings')

# Get the Django WSGI application
django_app = get_wsgi_application()

# Serve static files with WhiteNoise
try:
    BASE_DIR = Path(__file__).resolve().parent.parent
    static_root = BASE_DIR / 'staticfiles'
    
    # Ensure static root exists
    if not static_root.exists():
        print(f"Warning: Static files directory not found at {static_root}", file=sys.stderr)
    
    app = WhiteNoise(
        django_app,
        root=str(static_root),
        prefix='static/',
        index_file=True,
        mimetypes={
            '.js': 'application/javascript; charset=utf-8',
            '.css': 'text/css; charset=utf-8',
        }
    )
    print(f"WhiteNoise configured to serve from: {static_root}", file=sys.stderr)
except Exception as e:
    print(f"Error configuring WhiteNoise: {e}", file=sys.stderr)
    app = django_app


