from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic.list import ListView
from blogapp.models import PostBlog
from blogapp.forms import BlogForm
from django.utils import timezone
import datetime


class HomeView(View):
    """
    Admin Panel page view
    """
    def get(self, request):
        """
        Function to render Admin panel page
        """
        if request.user.is_staff:
            return render(request, 'adminpanel/hello.html')
        else:
            return render(request, 'adminpanel/index.html')


class IndexView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'adminpanel/index.html')


class ListBlog(ListView):
    """
    class for blog list to show
    """
    model = PostBlog
    form_class = BlogForm
    template_name = "adminpanel/bloglists.html"

    def get(self, request):
        """
        get function to resrict access to certain users
        """
        object_list = PostBlog.objects.all()
        if request.user.is_staff:
            return render(request, "adminpanel/bloglists.html", {'object_list':object_list})
        else:
            return render(request, 'adminpanel/index.html')

    def choices(self):
        """
        function to return only published blogs
        """
        return PostBlog.objects.filter(status=1)


def published(request, pk):
    """
    function to change status to published
    """
    blog = PostBlog.objects.get(id=pk)
    blog.status = 1
    date = timezone.now()
    blog.published_date = timezone.now()
    a = 1
    blog.save()
    return redirect('adminpanel:listblog')

def unpublished(request, pk):
    """
    function to change status to unpublished
    """
    blog = PostBlog.objects.get(id=pk)
    blog.status = 2
    blog.published_date = None
    blog.save()
    return redirect('adminpanel:listblog')

def publish_date(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.published_date = timezone.now()
    blog.save()
    return redirect('adminpanel:listblog')


class AdminView(View):
    """
    Class which has a function which returns number of active users
    """
    def get(self, request):
        """
        Function which returns number of active users
        """
        usercount = User.objects.filter(is_active=True).count()
        return JsonResponse(usercount, safe=False)


class AdView(View):
    """
    Class which has a function which returns number of superuser users
    """
    def get(self, request):
        """
        Function which returns number of superuser users
        """
        superuser = User.objects.filter(is_superuser=True).count()
        return JsonResponse(superuser, safe=False)


class NormalView(View):
    """
    Class which has a function which returns number of normal users
    """
    def get(self, request):
        """
        Function which returns number of normal users
        """
        normaluser = User.objects.filter(is_superuser=False).count()
        return JsonResponse(normaluser, safe=False)


class MyUserView(View):
    """
    Class to restrict access to certain page for users
    """
    def get(self, request):
        """
        get Function to restrict access to certain page for users
        """
        users = User.objects.all()
        if self.request.user.is_superuser:
            return render(request, 'adminpanel/hey.html', {'users': users})
        else:
            return redirect("/")


class MyStatusView(View):
    """
    User Status view
    """
    def get(self, request, *args, **kwargs):
        """
        Function to render User Status page
        """
        users = User.objects.all()
        user_id = kwargs['pk']
        user = User.objects.get(pk=user_id)
        if request.user.is_superuser:
            if user.is_superuser:
                user.is_superuser=False
                user.save()
            else:
                user.is_superuser=True
                user.save()

        return render(request, 'adminpanel/hey.html', {'users': users})
