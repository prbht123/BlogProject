from django.db import models
from blogapp.models import PostBlog
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class BlogCommentModel(models.Model):
    author = models.ForeignKey(User,related_name='blogcommmentmodel_author', default=None,on_delete=models.CASCADE)
    blogpost = models.ForeignKey(PostBlog, related_name='blogcommmentmodel_comment', on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField( unique=True)

    def unique_slug(self):
        unique_slugg = slugify(self.comment)
        num = 1
        while BlogCommentModel.objects.filter(slug=unique_slugg).exists():
            unique_slugg = "{}-{}".format(unique_slugg,num)
            num += 1
            break
        return unique_slugg

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = self.unique_slug()
      return super().save(*args, **kwargs)


    # Function to return title on table
    def __str__(self):
        return self.comment