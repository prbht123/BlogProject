from django.urls import path
from adminpanel.views import HomeView, AdminView, AdView, NormalView, MyUserView, MyStatusView, IndexView, ListBlog
from adminpanel import views


app_name = 'adminpanel'

urlpatterns = [
    path('home/', HomeView.as_view(), name="home"),
    path('index/', IndexView.as_view(), name="index"),
    path('getUser/', AdminView.as_view(), name="adminn"),
    path('getSuper/', AdView.as_view(), name="ad"),
    path('getNormal/', NormalView.as_view(), name="normaluser"),
    path('userstatus/', MyUserView.as_view(), name='userstatus'),
    path('status/<int:pk>', MyStatusView.as_view(), name='status'),
    path('lists/',views.ListBlog.as_view(),name='listblog'),
    path('unpublished/<int:pk>/', views.unpublished, name='unpublished'),
    path('published/<int:pk>/', views.published, name='published')
]
    