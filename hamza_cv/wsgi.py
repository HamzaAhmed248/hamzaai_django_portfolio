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

try:
	app = get_wsgi_application()
	
	# Wrap with WhiteNoise for static files
	BASE_DIR = Path(__file__).resolve().parent.parent
	app = WhiteNoise(app, root=str(BASE_DIR / 'staticfiles'))
except Exception as e:
	import sys, traceback
	tb = traceback.format_exc()
	print("WSGI startup error:\n" + tb, file=sys.stderr)
	raise
