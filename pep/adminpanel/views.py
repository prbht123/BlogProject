from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.generic.list import ListView
from blogapp.models import PostBlog
from blogapp.forms import BlogForm


class HomeView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
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
    model = PostBlog
    form_class = BlogForm
    template_name = "adminpanel/bloglists.html"

    def choices(self):
        return PostBlog.objects.filter(status=1)

def published(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 1
    blog.save()
    print(request.POST)
    print("000000000000011111111111111")
    return redirect('adminpanel:listblog')

def unpublished(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 2
    blog.published_date = None
    blog.save()
    print(request.POST)
    print("000000000000011111111111111")
    return redirect('adminpanel:listblog')


class AdminView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        # queryset = models.User.objects.filter(is_active=True).count()
        usercount = User.objects.filter(is_active=True).count()
        return JsonResponse(usercount, safe=False)

class AdView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        # queryset = models.User.objects.filter(is_active=True).count()
        superuser = User.objects.filter(is_superuser=True).count()
        return JsonResponse(superuser, safe=False)

class NormalView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        # queryset = models.User.objects.filter(is_active=True).count()
        normaluser = User.objects.filter(is_superuser=False).count()
        return JsonResponse(normaluser, safe=False)


class MyUserView(View):
    """
    User Status view
    """
    def get(self, request):
        """
        Function to render User Status page
        """
        # context = User.objects.all()
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
        # user = User.objects.filter(pk=3)
        # user.is_superuser = True
        # user.is_staff = True
        # user.save()

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

