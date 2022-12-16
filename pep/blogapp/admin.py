from django.contrib import admin
from blogapp.models import BlogCategory, PostBlog, TagBlog

# Registering models on admin site
admin.site.register(BlogCategory)
admin.site.register(PostBlog)
admin.site.register(TagBlog)
