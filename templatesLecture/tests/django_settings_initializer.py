import os
import django

# Initialize Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'templatesLecture.settings')  # Adjust to your project
django.setup()


"""
    I use this to initialize my Django Settings inside this tests directory
    This is a must because this Tests directory is not inside specific application
    That's why i need to initialize in order to make imports from django library like `from django.unittest import TestCase`
"""