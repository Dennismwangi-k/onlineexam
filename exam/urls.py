from django.urls import path

from exam.views import account_views, admin_views, app_views
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from django.conf.urls.static import static
from django.conf import settings
urlpatterns = [

        ## Account views
    path('accounts/register/', account_views.register, name='register'),
    path('accounts/register/<str:invited_by_username>/', account_views.register, name='register_invited'),
    path('accounts/login/',account_views.login,name='login'),
    path('accounts/logout/',account_views.logout_view,name='logout'),
    path('accounts/profile/',account_views.profile,name='profile'),
    path('accounts/profile_update/<int:user_id>/',account_views.profile_update,name='profile_update'),
    path('accounts/change-password/', account_views.change_password, name='change_password'),



    #Password Reset
    path('password-reset/', PasswordResetView.as_view(template_name='accounts/password_reset.html',
        subject_template_name='accounts/password_reset_subject.txt',),name='password-reset'),
    path('password-reset/done/', PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html'),name='password_reset_complete'),
 
    path('', app_views.index, name='index'),
    path('exam', app_views.exam, name='exam'),
    path('about', app_views.about, name='about'),
    path('contact', app_views.contact, name='contact'),
    path('services', app_views.services, name='services'),
    path('blog', app_views.blog, name='blog'),
    path('test', app_views.test, name='test'),

]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
