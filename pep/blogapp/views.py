from django.shortcuts import render, redirect, HttpResponse
from .models import BlogCategory, PostBlog, TagBlog
from .forms import BlogForm
from django.views import View
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse


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
    # form_class = BlogForm
    template_name = "blogapp/postblog_update.html"
    # print(form_class)
    # print("____________________________________000000000")

    def form_valid(self, form):
        # print(self.request.POST)
        tag_data = self.request.POST['tagname']
        tagging  = tag_data.split(' ')
        data = form.save()
        # print(">.....>>>>>>>>>>>>>>>>.........")
        # print(tagging)

        for tag in tagging:
            try:
                var = TagBlog.objects.get(name=tag)
                taggers = data.tags.all()
                # print(taggers)
                if var in tagging:
                    continue
                else:
                    data.tags.add(var)

            except:
                data.tags.create(name=tag)

        status_data = self.request.POST['status']
        print(status_data)
        # if self.request.user.is_superuser:
        #     data.status.create(status=status_data)
        # else:
        #     return HttpResponse("Access denied")

        return redirect('blogapp:create')

    def dispatch(self, request, *args, **kwargs ):
        if request.user.is_superuser:
            self.fields = ['title', 'content', 'image','category','status']
        else:
            self.fields = ['title', 'content', 'image','category']
        return super().dispatch(request, *args, **kwargs)


class BlogDetail(DetailView):
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_detail.html"

    # def get(self, request, *args, **kwargs):
    #     option = 
    #     return render(request, 'blogapp/postblog_detail.html', context)

def publish(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 1
    blog.save()
    print(request.POST)
    print("000000000000011111111111111")
    return redirect('blogapp:detail', pk=blog.id)

def unpublish(request, pk):
    blog = PostBlog.objects.get(id=pk)
    blog.status = 2
    blog.published_date = None
    blog.save()
    print(request.POST)
    print("000000000000011111111111111")
    return redirect('blogapp:detail', pk=blog.id)

def remove(request, pk):
    blog = PostBlog.objects.get(id=pk)
    print(request.user.is_staff)
    if blog.blogger == request.user or request.user.is_staff:
        return redirect('blogapp:delete', pk=blog.id)
    else:
        return HttpResponse("not authorized!!!!")
    return redirect('blogapp:detail', pk=blog.id)

def edit(request, pk):
    blog=PostBlog.objects.get(id=pk)
    if blog.blogger == request.user or request.user.is_staff:
        return redirect('blogapp:update',pk=blog.id)
    else:
        return HttpResponse("not authorized to update!!!!")


class SearchView(ListView):
    model = PostBlog
    
    def get(self, request):
       
       query = self.request.GET['q']
       print(query)
       result = PostBlog.objects.filter(title__icontains=query)
       
       print(result)
       msg = None
       if not result:
        msg = "Result Not Found"
       searched={'result':result,'msg':msg}
       print("0000000000000000000000000000000")
       print(searched)
       return render(request,'blogapp/postblog_list.html',searched)


    # def get(self, request, *args, **kwargs):
    #     """
    #     Function to render home page
    #     """
    #     pass
    #     # stats = PostBlog.objects.all()
    #     # stat_id = kwargs['pk']
    #     # data=form.save()
    #     # option = self.request.POST['Publish']
    #     # print("0000000000000000000")
    #     # print(option)
    #     # data=form.save()
    #     # # stat = PostBlog.objects.filter(pk=stat_id)
    #     # choice = PostBlog.objects.get(pk=stat_id)
    #     # # print(stat)
    #     # print(choice)
    #     # print(choice.status)
    #     # if self.request.user.is_superuser:
    #     #     if choice.status == '0' or '2':
    #     #         choice.status = 1
    #     #         print("...........")
    #     #         choice.save()

    #     # elif choice.status == '1' :
    #     #     choice.status = 1
    #     #     print("###################################44444.")
    #     #     choice.save()
    #     # statuspublish = 
    #     # return redirect('blogapp:detail', pk =stat_id)
    #     print(args)
    #     context={}
    #     context['object'] = PostBlog.objects.get(pk=kwargs['pk'])
    #     print("000000000000000000000000000000")
    #     if 'Published' in self.kwargs.keys():
    #         print('Published')
    #     # print(self.kwargs.__dict__)
    #     return render(request, 'blogapp/postblog_detail.html', context)

class PublishView(View):

    def get(self, request, *args, **kwargs):
        """
        Function to render home page
        """
        # queryset = models.User.objects.filter(is_active=True).count()
        stats = PostBlog.objects.all()
        stat_id = kwargs['pk']
        stat = PostBlog.objects.get(pk=stat_id)
        # statuspublish = 
        return render(request, 'blogapp/detail.html', {'stats': stats})
        # return JsonResponse(statuspublish, safe=False)

    # def get(self, request, *args, **kwargs):

    #     author = 
    
    # def post(self, request, *args, **kwargs):
    #     stats = self.request.POST
    #     print("00000000000000000000000000000000000")

    #     print(stats)
    #     return redirect('blogapp:detail')

    # def form_valid(self, form):
    #     status = form.save()
    #     print(status)
    #     return redirect('blogapp:list')


class BlogDelete(DeleteView):
    model = PostBlog
    template_name = "blogapp/postblog_confirm_delete.html"

    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('blogapp:create')


class BlogList(ListView):
    model = PostBlog
    form_class = BlogForm
    template_name = "blogapp/postblog_list.html"

    def choices(self):
        return PostBlog.objects.filter(status=1)
