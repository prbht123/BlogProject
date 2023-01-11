from django.db import models
from blogapp.models import PostBlog
from django.contrib.auth.models import User
from django.template.defaultfilters import slugify


class BlogCommentModel(models.Model):
    """
    Comment Model for blogs to create a comment table
    """
    author = models.ForeignKey(User,related_name='blogcommmentmodel_author', default=None,on_delete=models.CASCADE)
    blogpost = models.ForeignKey(PostBlog, related_name='blogcommmentmodel_comment', on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    likes = models.ManyToManyField(User, related_name='commentlike_user')
    dislikes = models.ManyToManyField(User, related_name='commentdislike_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField( unique=True)

    # Function to count no. of likes
    def total_likes(self):
        return self.likes.count()
    
    # Function to count no. of dislikes
    def total_dislikes(self):
        return self.dislikes.count()
    
    # Function to return unique slug
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


class BlogRatingModel(models.Model):
    """
    Rating Model to create a Rating table for blogs 
    """
    RATING_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    rater = models.ForeignKey(User,related_name='blogratingmodel_rater', default=None, on_delete=models.CASCADE)
    post = models.ForeignKey(PostBlog, related_name='blogratingmodel_post', on_delete=models.CASCADE)
    rating = models.CharField(max_length=1, choices = RATING_CHOICES, null=True, blank=True)
    slug = models.SlugField( unique=True)

    # Function to return unique slug
    def unique_slug(self):
        unique_slugg = slugify(self.rating)
        num = 1
        while BlogRatingModel.objects.filter(slug=unique_slugg).exists():
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
        return self.rating
