from django.urls import path, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from mypep.views import MyView, SignUpView, UserLogin, ProfileUpdate, ProfileDetail, MyDetailView


app_name = "mypep"

urlpatterns = [
    path('', MyView.as_view(), name="base"),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', UserLogin.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='mypep:login'), name='logout'),

    path('update/<int:pk>', ProfileUpdate.as_view(), name='update'),
    # path('detail/', ProfileDetail.as_view(), name='detail'),
    path('detail/', MyDetailView.as_view(), name='detail'),

    path('change/', auth_views.PasswordChangeView.as_view(template_name="mypep/password_change_form.html",
                                                          success_url=reverse_lazy('mypep:password_change_done')), name='password_change'),
    path('change_done/', auth_views.PasswordChangeDoneView.as_view(template_name="mypep/password_change_done.html",),
                                                                  name='password_change_done'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='mypep/password_reset_form.html', success_url=reverse_lazy('mypep:password_reset_done')),
    name='password_reset'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='mypep/password_reset_done.html'),
    name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='mypep/password_reset_confirm.html', success_url=reverse_lazy('mypep:password_reset_complete')),
    name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='mypep/password_reset_complete.html'),
    name='password_reset_complete')
]
