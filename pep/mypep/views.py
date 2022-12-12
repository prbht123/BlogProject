from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView,UpdateView
from django.views.generic.detail import DetailView
from django.views import View
from django.urls import reverse_lazy
from mypep.forms import SignUpForm


class UserLogin(LoginView):
    """
    LoginView which by default provides us with a form
    """
    template_name = 'mypep/login.html'
    fields = "__all__"
    redirect_authenticated_user = True
    success_url = reverse_lazy('mypep:base')


class SignUpView(CreateView):
    """
    Created SignupView which has SignUpForm for user registraion
    """
    form_class = SignUpForm
    success_url = reverse_lazy('mypep:base')
    template_name = 'mypep/signup.html'

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignUpView, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('mypep:base')
        return super(SignUpView, self).get(*args, **kwargs)


class MyView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'mypep/hello.html')


class ProfileUpdate(UpdateView):
    model = 'ProfileModel'
    fields = '__all__'


class ProfileDetail(DetailView):
    model = 'ProfileModel'
    fields = '__all__'


class MyDetailView(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'mypep/profilemodel_detail.html')