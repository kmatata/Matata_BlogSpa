from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('post/<slug:slug>/',views.single_post,name="postDetails"),
    path('about-us/',views.about,name='about-us')
]