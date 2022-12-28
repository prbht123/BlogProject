from django.shortcuts import render, redirect, HttpResponse
from .models import BlogCategory, PostBlog, TagBlog
from .forms import BlogForm
from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy, reverse
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponseRedirect
from blogcomment.forms import BlogCommentForm, BlogRatingForm
from blogcomment.models import BlogCommentModel, BlogRatingModel
from mypep.models import ProfileModel
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.db.models import Avg
from decimal import Decimal
from django.db.models import Func


class Blogging(View):
    """
    Home page view
    """
    # Function to render home page
    def get(self, request):
        return render(request, 'blogapp/home.html')


class BlogCreate(LoginRequiredMixin, CreateView):
    """
    To create a blog form
    """
    login_url = '/mypep/login'
    redirect_field_name = 'login'

    form_class = BlogForm
    template_name = "blogapp/postblog_form.html"
    success_url = reverse_lazy('blogapp:create')

    # Function if the form is valid
    def form_valid(self, form):
            tag_data = self.request.POST['tagname']
            tagging  = tag_data.split(',')
            data = form.save(commit=False)
            data.blogger = self.request.user
            data.save()
            for tag in tagging:
                try:
                    var = TagBlog.objects.get(name=tag)
                    data.tags.add(var)
                except:
                    data.tags.create(name=tag)
            return redirect('blogapp:create')


class BlogUpdate(LoginRequiredMixin, UpdateView):
    """
    To update a blog form
    """
    login_url = '/mypep/login'
    redirect_field_name = 'login'
    model = PostBlog
    template_name = "blogapp/postblog_update.html"

    # Function to perform operations if the form is valid
    def form_valid(self, form):
        tag_data = self.request.POST['tagname']
        tagging  = tag_data.split(' ')
        data = form.save()

        for tag in tagging:
            try:
                var = TagBlog.objects.get(name=tag)
                taggers = data.tags.all()
                if var in tagging:
                    continue
                else:
                    data.tags.add(var)
            except:
                data.tags.create(name=tag)

        status_data = self.request.POST['status']
        return redirect('blogapp:create')

    # dispatch function to show particular fields 
    def dispatch(self, request, *args, **kwargs ):
        if request.user.is_superuser:
            self.fields = ['title', 'content', 'image','category','status']
        else:
            self.fields = ['title', 'content', 'image','category']
        return super().dispatch(request, *args, **kwargs)


class BlogDetail(DetailView):
    """
    class to show blog details
    """
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_detail.html"

    # function to get context data
    def get_context_data(self,  *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = BlogCommentForm()
        blog_id = self.kwargs['pk']
        blog = get_object_or_404(PostBlog, id=self.kwargs['pk'])
        comments = BlogCommentModel.objects.order_by('-created_at').filter(blogpost=blog_id)[:5]
        like_number = blog.number_of_likes()
        like = False
        if blog.likes.filter(id=self.request.user.id).exists():
            like = True
        dislike_number = blog.number_of_dislikes()
        dislike = False
        if blog.dislikes.filter(id=self.request.user.id).exists():
            dislike = True
        ratings = BlogRatingModel.objects.filter(post=blog_id)
        lst = []
        for i in ratings:
            lst.append(i.rater)
        if self.request.user not in lst:
            context["ratingform"] = BlogRatingForm()
        rating_avg = BlogRatingModel.objects.filter(post=blog_id).aggregate(Avg('rating'))
        rate = {}
        rate = rating_avg
        rate_avg = rate.get('rating__avg')
        context["comment_list"] = comments
        context["like_number"] = like_number
        context["like"] = like
        context["dislike_number"] = dislike_number
        context["dislike"] = dislike
        context["list"] = lst
        context["rate_avg"] = rate_avg
        return context


# this function is called if the post is liked
def postLike(request, pk):
    blog = PostBlog.objects.get(id=pk)

    if blog.likes.filter(id=request.user.id).exists():
        blog.likes.remove(request.user)
    else:
        if blog.dislikes.filter(id=request.user.id).exists():
            blog.dislikes.remove(request.user)
        blog.likes.add(request.user)

    return redirect('blogapp:detail', pk=blog.id)


# this function is called if the post is disliked
def postDisLike(request, pk):
    blog = PostBlog.objects.get(id=pk)
    if blog.dislikes.filter(id=request.user.id).exists():
        blog.dislikes.remove(request.user)
    else:
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
        blog.dislikes.add(request.user)

    return redirect('blogapp:detail', pk=blog.id)


# function to change blog status from draft to publish
def publish(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 1
    blog.save()
    return redirect('blogapp:detail', pk=blog.id)

# function to change blog status from publish to unpublish
def unpublish(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 2
    blog.published_date = None
    blog.save()
    return redirect('blogapp:detail', pk=blog.id)


# Function to delete a blog
def remove(request, pk):
    blog = PostBlog.objects.get(id=pk)
    if blog.blogger == request.user or request.user.is_staff:
        return redirect('blogapp:delete', pk=blog.id)
    else:
        return HttpResponse("not authorized!!!!")
    return redirect('blogapp:detail', pk=blog.id)

# Function to update a blog
def edit(request, pk):
    blog=PostBlog.objects.get(id=pk)
    if blog.blogger == request.user or request.user.is_staff:
        return redirect('blogapp:update',pk=blog.id)
    else:
        return HttpResponse("not authorized to update!!!!")


class SearchView(ListView):
    """
    Class to get the search results
    """
    model = PostBlog

    # get Function to get the search results in blog list
    def get(self, request):
        query = self.request.GET['q']
        result = PostBlog.objects.filter(title__icontains=query)
        msg = None
        if not result:
            msg = "Result Not Found"
        searched={'result':result,'msg':msg}
        return render(request,'blogapp/postblog_list.html',searched)


class BlogDelete(DeleteView):
    """
    Class for deleting a blog
    """
    model = PostBlog
    template_name = "blogapp/postblog_confirm_delete.html"

    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blogapp:create')


class BlogList(ListView):
    """
    class to show the list of blogs
    """
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_list.html"

    # function to show only published blogs
    def choices(self):
        return PostBlog.objects.filter(status=1)
