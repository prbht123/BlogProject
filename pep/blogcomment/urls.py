from django.urls import path
from blogcomment import views
from blogcomment.views import BlogCommentCreate

app_name = "blogcomment"

urlpatterns = [
    path('detail/<int:pk>/commentcreate', BlogCommentCreate.as_view(), name="create"),
]
