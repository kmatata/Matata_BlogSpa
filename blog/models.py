from django.conf import settings
from enum import unique
from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User
from PIL import Image
import os

# Create your models here.

def blog_image_dir_path(instance, filename):
    image_ext = '.jpeg'
    try:
        if (filename[-4] == 'jpeg'):
            image_ext = '.jpeg'
        elif (filename[-3] == 'png'):
            image_ext = '.png'
        elif (filename[-3] == 'jpg'):
            image_ext = '.jpg'
    except Exception as e:
        raise e    
    image_ext_name = 'user_{0}/postImage{1}'.format(instance.author.id,image_ext)    
               

    return image_ext_name
class BlogPost(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE, related_name='myBlogPosts')
    post = models.TextField()
    title = models.CharField(max_length=200, unique=True)
    postImage = models.ImageField(upload_to=blog_image_dir_path,default=None,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True)
    def save(self,*args,**kwargs):
        super().save(*args,**kwargs)
        SIZE = 600,1200
        if self.postImage:
            img = Image.open(self.postImage.path)
            img.thumbnail(size=(SIZE))
            img.save(self.postImage.path, optimize=True, quality=90)
    class Meta:
        ordering = ['-created']

    @property
    def slug(self):
        return slugify(self.title)

    @property
    def summary(self):
        return self.post[:100] + "..."

    @property
    def get_absolute_url(self):
        return reverse("blog:postDetails", kwargs={"slug":self.slug})
    
    def __str__(self):
        return self.title


