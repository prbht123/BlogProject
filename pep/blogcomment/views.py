from django.shortcuts import render, redirect
from blogcomment.models import BlogCommentModel, BlogRatingModel
from blogcomment.forms import BlogCommentForm, BlogRatingForm
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.list import ListView
from blogapp.models import PostBlog
from django.contrib import messages

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


#this class is not in use
class RatingCreate(CreateView):
    """
    Class to create and save rating form
    """
    model = BlogRatingModel
    form_class = BlogRatingForm
    template_name ="blogcomment/blogratingmodel_form.html"

    def form_valid(self, form):
        form.instance.rater = self.request.user
        blog = PostBlog.objects.get(id=self.kwargs['pk'])
        form.instance.post = blog
        form.save()
        return redirect('blogapp:detail', pk = self.kwargs['pk'])


def rating(request, pk):
    """
    function to save rating form data
    """
    if request.method == "GET":
        post = PostBlog.objects.get(id=pk)
        rating = request.GET.get('rating')
        rater = request.user
        BlogRatingModel(rater=rater, post=post, rating=rating).save()
        return redirect('blogapp:detail', pk=post.id)