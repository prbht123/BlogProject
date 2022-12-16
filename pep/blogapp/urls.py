from django.urls import path
from blogapp import views
from blogapp.views import Blogging, BlogCreate

app_name = "blogapp"

urlpatterns = [
    path('', views.Blogging.as_view(),name="index"),
    path('create/', views.BlogCreate.as_view(),name="create"),
    path('update/<int:pk>/',views.BlogUpdate.as_view(),name='update'),
    path('detail/<int:pk>/',views.BlogDetail.as_view(),name='detail'),
    path('delete/<int:pk>/',views.BlogDelete.as_view(),name='delete')
]