# Datetime Imports
from datetime import datetime

# Django Imports
from django.utils import timezone


def get_now() -> datetime:
    """The current time"""
    return timezone.now()