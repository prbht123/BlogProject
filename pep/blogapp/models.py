from django.db import models
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class TagBlog(models.Model):
    """
        TagBlog model for tags of blog
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Function to return name on table
    def __str__(self):
        return self.name


class BlogCategory(models.Model):
    title =  models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField( unique=True)

    # Slugify Function
    def save(self, *args, **kwargs):
      if not self.slug:
         self.slug = slugify(self.title)
      return super().save(*args, **kwargs)

    # Function to return title on table
    def __str__(self):
        return self.title


class PostBlog(models.Model):
    """
        PostBlog model for blog details
    """
    STATUS_CHOICES = (
        ('0', 'Draft'),
        ('1', 'Publish'),
        ('2', 'Unpublish')
    )
    title = models.CharField(max_length=250)
    content = models.TextField(max_length=300, null=True, blank=True)
    image = models.ImageField(upload_to='blog', default="", null = True, blank=True)
    blogger = models.ForeignKey(User, related_name='postblog_blogger', on_delete=models.CASCADE)
    tags = models.ManyToManyField(TagBlog, related_name="postblog_tags")
    category = models.ForeignKey(BlogCategory, related_name="postblog_category", on_delete=models.CASCADE, null = True, blank=True )
    status = models.CharField(max_length=1, choices = STATUS_CHOICES, null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='bloglike_user')
    dislikes = models.ManyToManyField(User, related_name='blogdislike_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_date = models.DateTimeField(auto_now=True)
    slug = models.SlugField( unique=True)

    # Function to return number of likes
    def number_of_likes(self):
        return self.likes.count()

    # Function to return number of dislikes
    def number_of_dislikes(self):
        return self.dislikes.count()

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.title)
        num = 1
        while PostBlog.objects.filter(slug=unique_slugg).exists():
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
        return self.title
