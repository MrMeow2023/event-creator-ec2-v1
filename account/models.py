from django.db import models
from django.conf import settings
from uuid import uuid4

def avatar_url(instance, filename):
    ext = filename.split('.')[-1]
    return 'images/{0}/avatar/{1}.{2}'.format(
        instance.user.username,
        uuid4().hex,
        ext
    )
# Create your models here.  
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    description = models.CharField(max_length=100, default = "")
    avatar = models.ImageField(upload_to = avatar_url, default = "images/no_avatar.png")
    def __str__(self):
        return f"{self.user.username}"