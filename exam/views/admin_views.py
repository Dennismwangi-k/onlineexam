# customadmin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from exam.models import ExamUser, Questions

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from exam.forms import AdminProfileUpdateForm, AdminSetPasswordForm,ProfileUpdateForm
from django.db.models import Sum, IntegerField
from django.db.models.functions import Round
from django.contrib.auth.models import Group
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.views import PasswordChangeView
from exam.decorators import admin_only

@login_required
@admin_only
def admin_dashboard(request):
    total_users_count = ExamUser.objects.all().count()
    active_users_count = ExamUser.objects.all().filter(is_active=False).count()
    dormant_users_count = ExamUser.objects.all().filter(is_active=True).count()

    context = {
        'total_users_count': total_users_count,
        'active_users_count': active_users_count,
        'dormant_users_count': dormant_users_count,

    }

    return render(request, 'customadmin/dashboard.html', context)

@login_required
@admin_only
def all_users(request):
    users = ExamUser.objects.all()

    context = {
        'users': users,
        'table_title': "All Users"
    }
    return render(request, 'customadmin/users.html', context)

@login_required
@admin_only
def active_users(request):
    users = ExamUser.objects.filter(is_active=True).all()

    context = {
        'users': users,
        'table_title': "Active Users"
    }
    return render(request, 'customadmin/users.html', context)

@login_required
@admin_only
def dormant_users(request):
    users = ExamUser.objects.filter(is_active=False).all()

    context = {
        'users': users,
        'table_title': "Dormant Users"
    }
    return render(request, 'customadmin/users.html', context)


@login_required
@admin_only
def add_question(request):
    if request.method == 'POST':
        pass
    return render(request, 'customadmin/add_question.html')

@login_required
@admin_only
def edit_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if request.method == 'POST':
        pass
    context = {'question': question}
    return render(request, 'customadmin/edit_question.html', context)

@login_required
@admin_only
def delete_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if question:
        question.delete()
        return redirect('admin_dashboard')
    context = {'question': question}
    return render(request, 'customadmin/delete_question.html', context)

@login_required
@admin_only
def view_users(request):
    users = ExamUser.objects.all()
    context = {'users': users}
    return render(request, 'customadmin/view_users.html', context)


@login_required
@admin_only
def delete_user(request, user_id):
    user = get_object_or_404(ExamUser, pk=user_id)
    if user:
        user.delete()
        return redirect('admin_dashboard')
    messages.success(request, f'User deleted!')
    return redirect(request.META.get('HTTP_REFERER', '/'))

@login_required
@admin_only
def update_user(request, user_id):
  user = ExamUser.objects.get(pk=user_id)
  if request.method == 'POST':
    update_user_form = AdminProfileUpdateForm(request.POST,request.FILES, instance=user)
    if update_user_form.is_valid():
      update_user_form.save()
      messages.success(request, f'User updated!')
      previous_url = request.session.get('previous_url')
      if previous_url:
          del request.session['previous_url']
          return redirect(previous_url)
  else:
    update_user_form = AdminProfileUpdateForm(instance=user)
    request.session['previous_url'] = request.META.get('HTTP_REFERER')
  context = {
      "update_user_form":update_user_form,
      "user":user
  }
  return render(request, 'admin/update_user.html', context)