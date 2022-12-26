from django.shortcuts import render, redirect
from blogcomment.models import BlogCommentModel
from blogcomment.forms import BlogCommentForm
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from blogapp.models import PostBlog


class BlogCommentCreate(CreateView):
    """
    Class to create comments
    """
    model = BlogCommentModel
    form_class = BlogCommentForm
    template_name ="blogcomment/blogcommentmodel_form.html"

    # function will perform operations if the form is valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        blog = PostBlog.objects.get(id=self.kwargs['pk'])
        form.instance.blogpost = blog    
        form.save()
        return redirect('blogapp:detail', pk = self.kwargs['pk'])
  