from django.shortcuts import render
from django.views import View
from django.contrib.auth.models import User
from django.http import JsonResponse


class HomeView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'adminpanel/hello.html')


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


