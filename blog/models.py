from django.db import models
from django.utils import timezone
from django.urls import reverse
# import user model
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
    # redirect to the detail page of newly created post
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk':self.pk})