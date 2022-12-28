from django.contrib import admin
from blogcomment.models import BlogCommentModel, BlogRatingModel

# Register your models here.
admin.site.register(BlogCommentModel)
admin.site.register(BlogRatingModel)