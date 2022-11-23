from django.urls import path
from . import views

app_name = 'blog_authy'

urlpatterns = [
    path('login/',views.Login,name='login'),
    path('register/',views.Signup)
]