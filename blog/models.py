from typing import Any
from django.db import models
from django.contrib.auth import get_user_model
from account.forms import UserForm
from uuid import uuid4


User = get_user_model()
def image_url(instance, filename):
    ext = filename.split('.')[-1]
    return 'images/{0}/{1}.{2}'.format(
        instance.author.username,
        uuid4().hex,
        ext
    )
# Create your models here.

class Post(models.Model): 
    title = models.CharField(max_length=255, unique=True) 
    content = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to = image_url)
    slug = models.SlugField(default="", unique=True)
    attending = models.ManyToManyField(User, default=None, related_name="attend_event")
    likes = models.ManyToManyField(User, default=None, related_name="post_likes")

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, default=None, related_name="comment_likes")

    def __str__(self):
        return '%s - %s' % (self.post.title, self.title)
     