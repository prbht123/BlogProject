from django.urls import path
from adminpanel.views import HomeView, AdminView, AdView, NormalView

app_name = 'adminpanel'

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('getUser/', AdminView.as_view(), name="adminn"),
    path('getSuper/', AdView.as_view(), name="ad"),
    path('getNormal/', NormalView.as_view(), name="normaluser")
]
    