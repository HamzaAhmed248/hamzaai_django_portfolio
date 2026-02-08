"""
WSGI config for hamza_cv project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hamza_cv.settings')

# Create the WSGI application, but log full tracebacks to stderr on failure
try:
	application = get_wsgi_application()
except Exception:
	import sys, traceback
	tb = traceback.format_exc()
	print("WSGI startup error:\n" + tb, file=sys.stderr)
	raise
