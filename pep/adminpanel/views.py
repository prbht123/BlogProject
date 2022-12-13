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
        return render(request, 'adminpanel/hey.html', {'users': users})


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

