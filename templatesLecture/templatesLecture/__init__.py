from __future__ import absolute_import, unicode_literals

# Import Celery app instance
from .celery import app as celery_app

# Make Celery app available globally
__all__ = ('templatesLecture.posts',)
