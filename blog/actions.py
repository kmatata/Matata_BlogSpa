from django.shortcuts import render
from django.urls import reverse
from asgiref.sync import async_to_sync
from django.template.loader import render_to_string
from blog.models import BlogPost
from django.urls import reverse


POSTS_PER_PAGE = 5

def add_next_posts(self, data={}):
    page = int(data["page"])
    start_of_slice = (page - 1) * POSTS_PER_PAGE
    end_of_slice = start_of_slice + POSTS_PER_PAGE
    context = {        
        "posts": BlogPost.objects.all()[start_of_slice:end_of_slice],
        "next_page": page + 1,
        "is_last_page": (BlogPost.objects.count() // POSTS_PER_PAGE) == page,
        "page":"components/_posts.html"
    }

    self.send_html(
        {
            "selector": "#all-posts",
            "html": render_to_string("components/_posts.html",context),
            "append": True,
        }
    )
    # update page
    self .send_html(
        {
            "selector": "#paginator",
            "html": render_to_string("components/_pagination.html", context),
            "append": False,
        }
    )


def send_page(self,data={}):
    page = data['page']
    data_reverse = {}
    match page:
        case "all posts":
            context = {
                "posts": BlogPost.objects.all()[:POSTS_PER_PAGE],
                "next_page": 2,
                "is_last_page": (BlogPost.objects.count() // POSTS_PER_PAGE) == 2,
                "page": "components/_posts.html"
            }
            self.send_html(
                {
                    "selector":"#all-posts",
                    "html": render_to_string("components/_posts.html",context),
                    "append":False,
                    'url': reverse('all posts'),
                }
            )
            self.send_html(
                {
                    "selector":"#paginator",
                    "html": render_to_string("components/_pagination.html",context),
                    "append":False
                }
            )
            self.send_html(
                {
                    "selector":"#navigation",
                    "html": render_to_string("components/_nav.html",{"active_nav": "all posts"}),                    
                    "append":False
                }
            )
        case "about us":                 
            self.send_html(
                {
                    "selector":"#all-posts",
                    "html": render_to_string("about_us.html"),                    
                    "append":False,
                    'url': reverse('blog:about-us'),                    
                }
            )
            self.send_html(
                    {
                        "selector":"#navigation",
                        "html": render_to_string("components/_nav.html",{"active_nav": "about us"}),                    
                        "append":False
                    }
                )
            self.send_html(
                {
                    "selector":"#paginator",
                    "html": render_to_string("components/_pagination.html",{"page":"about_us.html"}),
                    "append":False,

                    
                }
            )
        case "postDetails":
            postid = (data["id"])
            post = BlogPost.objects.get(id=(postid))
            next_post = BlogPost.objects.filter(pk__gt=post.pk).order_by('pk').first()
            prev_post = BlogPost.objects.filter(pk__lt=post.pk).order_by('-pk').first()
            data_reverse = {"slug":post.slug}
            self.send_html(
                {
                    "selector": "#all-posts",
                    "html": render_to_string("components/_postdeets.html",{"post":post,"next":next_post,"previous":prev_post}),
                    "url": reverse("blog:postDetails", kwargs=data_reverse),
                }
            )
            self.send_html(
                {
                    "selector":"#paginator",
                    "html": render_to_string("components/_pagination.html",{"page":"components/_postdeets.html"}),
                    "append":False,

                    
                }
            )
            self.send_html(
                    {
                        "selector":"#navigation",
                        "html": render_to_string("components/_nav.html",{"active_nav": "all posts"}),                    
                        "append":False
                    }
                )