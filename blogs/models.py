from django.db import models
from django.contrib.auth.models import User, auth
from django.utils import timezone

# Create your models here.
# category model
class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=100, blank=False, null=False)
    
    def __str__(self) -> str:
        return self.name
    
#Blog model    
class Blog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, max_length=100, null=False, blank=False, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(max_length=10000, null=False, blank=False)
    date = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self) -> str:
        return self.description

    
#comment view
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(User, models.CASCADE, default=1)
    comment = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=timezone.now)
    
    def __str__(self) -> str:
        return self.comment 
    