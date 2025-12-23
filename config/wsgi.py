"""
WSGI config for smarteducation project.
"""
import os
import logging
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

application = get_wsgi_application()

logger = logging.getLogger(__name__)
logger.info("SmartEducation application started")