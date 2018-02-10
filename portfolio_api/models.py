from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

def file_upload_path(instance, filename):
    return 'uploads/user_{0}/{1}'.format(instance.id, filename.split('/')[-1])

class User(AbstractUser):
    email = models.EmailField(blank=False)
    first_name = models.CharField(blank=False, max_length=30)
    last_name = models.CharField(blank=False, max_length=30)
    short_bio = models.TextField(blank=True, max_length=300)
    image = models.ImageField(upload_to=file_upload_path, blank=True)
    resume = models.FileField(upload_to=file_upload_path, blank=True)
    website = models.URLField(blank=True)
    github_profile = models.URLField(blank=True)
    linkedin_profile = models.URLField(blank=True)
