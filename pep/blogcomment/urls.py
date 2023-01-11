from django.urls import path
from blogcomment import views
from blogcomment.views import BlogCommentCreate, RatingCreate, BlogCommentUpdate

app_name = "blogcomment"

urlpatterns = [
    path('detail/<int:pk>/commentcreate', BlogCommentCreate.as_view(), name="create"),
    path('detail/<int:pk>/rating', views.rating, name='rate'),
    path('detail/<int:pk>/commentupdate', BlogCommentUpdate.as_view(), name="comment_update"),
    path('detail/<int:pk>/commentedit', views.BlogCommentEdit, name="comment_edit"),
    path('detail/<int:pk>/commentremove', views.BlogCommentRemove, name="comment_remove"),
    path('liked/', views.like_comment, name='liked'),
    path('disliked/', views.dislike_comment, name='disliked')
]
