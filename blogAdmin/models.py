from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.conf import settings
import os
from django.db.models.signals import post_save

# Create your models here.

def user_directory_path_profile(instance, filename):
    # file will be uploaded to MEDIA_ROOOT/user_id/filename       
    profile_pic_name = 'user_{0}/profile{1}'.format(instance.user.id,filename)    
    full_path  = os.path.join(settings.MEDIA_ROOT, profile_pic_name)
    
    if os.path.exists(full_path):
        os.remove(full_path)        

    return profile_pic_name



class Adminprofile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    location = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=80, null=True, blank=True)
    profile_info = models.TextField(max_length=100, null=True, blank=True)
    created = models.DateField(auto_now_add=True)
    picture = models.ImageField(upload_to=user_directory_path_profile)
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SIZE = 300, 300

        if self.picture:
            pic = Image.open(self.picture.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.picture.path)

    def __str__(self):
        return self.user.username

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Adminprofile.objects.create(user=instance)

def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)


