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

    ##Admin Views
    path('customadmin/dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),
    path('customadmin/add_question/', admin_views.add_question, name='admin_add_question'),
    path('customadmin/edit_question/<str:question_id>/', admin_views.edit_question, name='admin_edit_question'),
    path('customadmin/delete_question/<str:question_id>/', admin_views.delete_question, name='admin_delete_question'),

    path('customadmin/all_users/', admin_views.all_users, name='admin_view_all_users'),
    path('customadmin/active_users/', admin_views.active_users, name='admin_view_active_users'),
    path('customadmin/dormant_users/', admin_views.dormant_users, name='admin_view_dormant_users'),
    path('customadmin/update_user/<str:user_id>', admin_views.update_user,name='admin_update_user'),
    path('customadmin/delete_user/<str:user_id>/', admin_views.delete_user, name='admin_delete_user'),

]
if settings.DEBUG:
  urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
