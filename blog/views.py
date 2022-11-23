from django.shortcuts import render
from .models import BlogPost
# Create your views here.
BLOG_POSTS_PER_PAGE = 5
def index(request):
    return render(
        request,
        "base.html",
        {
            "posts": BlogPost.objects.all()[:5],
            "page": "components/_posts.html",
            "active_nav": "all posts",
            "next_page": 2,
            "is_last_page": (BlogPost.objects.count() // BLOG_POSTS_PER_PAGE) == 2,
        },
    )

def about(request):
    return render(
        request,
        "base.html",
        {
            "page": "about_us.html",
            "active_nav":"about us",
        },
    )

def single_post(request, slug):
    post = list(filter(lambda post: post.slug == slug, BlogPost.objects.all()))[0]
    return render(
        request,
        "base.html",
        {
            "post":post,
            "active_nav":"all posts",
            "page": "components/_postdeets.html"
        },
    )

