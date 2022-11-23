# Generated by Django 4.1.3 on 2022-11-23 09:34

import blog.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogPost",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("post", models.TextField()),
                ("title", models.CharField(max_length=200, unique=True)),
                (
                    "postImage",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to=blog.models.blog_image_dir_path,
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="myBlogPosts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-created"],},
        ),
    ]
