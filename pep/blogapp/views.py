from django.shortcuts import render, redirect
from .models import BlogCategory, PostBlog, TagBlog
from .forms import BlogForm
from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.views.generic.detail import DetailView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin


class Blogging(View):
    """
    Home page view
    """
    def get(self, request):
        """
        Function to render home page
        """
        return render(request, 'blogapp/home.html')


class BlogCreate(LoginRequiredMixin, CreateView):
    """
    To create blog on filling form
    """
    login_url = '/mypep/login'
    redirect_field_name = 'login'

    form_class = BlogForm
    template_name = "blogapp/postblog_form.html"
    success_url = reverse_lazy('blogapp:create')

    # def get_template_name(self):
    #     if self.request.user.is_authenticated:
    #         print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2")
    #         return "blogapp/postblog_form.html"
    #     else:
    #         print("################################")
    #         return redirect('mypep:login')

    def form_valid(self, form):
            """
            Function to perform operations 
            """
            print(self.request.POST)
            print("__________________________________")
            tag_data = self.request.POST['tagname']
            tagging  = tag_data.split(',')

            # if self.request.POST['category']:
            #     category_data = BlogCategory.objects.get(id=self.request.POST['category'])
            #     data.category = category_data

            # print(type(category_data))
            # print(category_data)
            # data = form.save(self.request.POST,self.request.FILES,commit=False)

            data = form.save(commit=False)
            # if category_data :
            #     data.category = category_data
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
    login_url = '/mypep/login'
    redirect_field_name = 'login'
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_update.html"
    print(form_class)
    print("____________________________________000000000")

    def form_valid(self, form):
        print(self.request.POST)
        tag_data = self.request.POST['tagname']
        tagging  = tag_data.split(' ')
        data = form.save()
        print(">.....>>>>>>>>>>>>>>>>.........")
        print(tagging)

        for tag in tagging:
            try:
                var = TagBlog.objects.get(name=tag)
                taggers = data.tags.all()
                print(taggers)
                if var in tagging:
                    continue
                else:
                    data.tags.add(var)

            except:
                data.tags.create(name=tag)

        return redirect('blogapp:create')


class BlogDetail(DetailView):
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_detail.html"


class BlogDelete(DeleteView):
    model = PostBlog
    template_name = "blogapp/postblog_confirm_delete.html"

    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blogapp:create')