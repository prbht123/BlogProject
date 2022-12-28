from django.urls import path
from blogcomment import views
from blogcomment.views import BlogCommentCreate, RatingCreate

app_name = "blogcomment"

urlpatterns = [
    path('detail/<int:pk>/commentcreate', BlogCommentCreate.as_view(), name="create"),
    # path('detail/<int:pk>/rating', RatingCreate.as_view(), name="rate")
    path('detail/<int:pk>/rating', views.rating, name='rate')
]
