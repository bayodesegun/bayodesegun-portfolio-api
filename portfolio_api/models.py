from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

def file_upload_path(instance, filename):
    id = None
    if isinstance(instance, User):
        id = instance.id
    elif isinstance(instance, Screenshot):
        id = instance.project.user.id
    
    return 'uploads/user_{0}/{1}'.format(id, filename.split('/')[-1])

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

class Project(models.Model):
    name = models.CharField(max_length=50)
    short_description = models.CharField(max_length=100)
    full_description = models.TextField(max_length=1000, blank=True)
    tech_stack = models.CharField(max_length=200)
    role = models.TextField(max_length=300)
    private = models.BooleanField(default=False)
    live_url = models.URLField(blank=True)
    repo_url = models.URLField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Screenshot(models.Model):
    image = models.ImageField(upload_to=file_upload_path, blank=False)
    caption = models.CharField(max_length=50)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
