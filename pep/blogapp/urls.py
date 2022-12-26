from django.urls import path
from blogapp import views
from blogapp.views import Blogging, BlogCreate, publish
from django.conf import settings
from django.conf.urls.static import static

app_name = "blogapp"

urlpatterns = [
    path('', views.Blogging.as_view(),name="index"),
    path('create/', views.BlogCreate.as_view(),name="create"),
    path('update/<int:pk>/',views.BlogUpdate.as_view(),name='update'),
    path('detail/<int:pk>/',views.BlogDetail.as_view(),name='detail'),
    path('delete/<int:pk>/',views.BlogDelete.as_view(),name='delete'),
    path('list/',views.BlogList.as_view(),name='list'),
    path('publish/<int:pk>/', views.publish, name='publish'),
    path('unpublish/<int:pk>/', views.unpublish, name='unpublish'),
    path('remove/<int:pk>/', views.remove, name='remove'),
    path('edit/<int:pk>/', views.edit, name='edit'),
    path('results/', views.SearchView.as_view(), name='search'),
    path('like/<int:pk>/', views.postLike, name='like'),
    path('dislike/<int:pk>/', views.postDisLike, name='dislike')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)