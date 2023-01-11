from django.shortcuts import render, redirect, HttpResponse
from blogcomment.models import BlogCommentModel, BlogRatingModel
from blogcomment.forms import BlogCommentForm, BlogRatingForm
from django.views.generic.edit import CreateView,UpdateView, DeleteView
from django.views.generic.list import ListView
from blogapp.models import PostBlog
from django.contrib import messages
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404


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


class BlogCommentUpdate(UpdateView):
    """
    Class to update a comment
    """
    model = BlogCommentModel
    form_class = BlogCommentForm
    template_name = 'blogcomment/blogcommentmodel_update.html'

    # function when the form is valid
    def form_valid(self, form):
        form.instance.author = self.request.user
        blog = PostBlog.objects.get(id=self.kwargs['pk'])
        form.instance.blogpost = blog    
        form.save()
        return redirect('blogapp:detail', pk = self.kwargs['pk'])


# function to allow specific users to update a comment
def BlogCommentEdit(request, pk):
    comment = BlogCommentModel.objects.get(id=pk)
    if comment.author == request.user :
        return redirect('blogcomment:comment_update',pk=comment.id)
    else:
        return HttpResponse("not authorized to update!!!!")


# function to delete a comment
def BlogCommentRemove(request, pk):
    comment = BlogCommentModel.objects.get(id=pk)
    post = comment.blogpost
    if comment.author == request.user or request.user == post.blogger:
        comment.delete()
        return redirect('blogapp:detail',pk=post.id)
    else:
        return HttpResponse("not authorized to delete!!!!")


# this function is called if the comment is liked
def like_comment(request):
    comment = get_object_or_404(BlogCommentModel, id=request.POST.get('liked'))    
    post = comment.blogpost
    is_liked = False
    if comment.likes.filter(id=request.user.id).exists():
        comment.likes.remove(request.user)
        is_liked = False
    else:
        if comment.dislikes.filter(id=request.user.id).exists():
            comment.dislikes.remove(request.user)
        comment.likes.add(request.user)
        is_liked = True
    return redirect('blogapp:detail', pk=post.id)


# this function is called if the comment is disliked
def dislike_comment(request):
    comment = get_object_or_404(BlogCommentModel, id=request.POST.get('disliked'))    
    post = comment.blogpost
    is_disliked = False
    if comment.dislikes.filter(id=request.user.id).exists():
        comment.dislikes.remove(request.user)
        is_disliked = False
    else:
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
        comment.dislikes.add(request.user)
        is_disliked = True
    return redirect('blogapp:detail', pk=post.id)
