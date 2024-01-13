from django import forms
from django.contrib.auth.decorators import login_required

from django.contrib import messages

from django.contrib.auth import authenticate
from django.shortcuts import render, redirect, get_object_or_404, HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login

from django.http import HttpResponse, Http404
from django.contrib.auth.models import Group

from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash


from exam.models import ExamUser


from exam.forms import CustomPasswordChangeForm, ProfileUpdateForm, RegistrationForm

def register(request):
    form = RegistrationForm(request.POST or None)

    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.phone = form.cleaned_data['phone']
            new_user.save()

            # Redirect to the login page after successful registration
            return redirect('login')

    return render(request, 'accounts/signup.html', {'form': form})


def login(request):
  if request.method == 'POST':
    form = AuthenticationForm(request=request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        auth_login(request, user)
        if user.groups.filter(name="Admin").exists():
            return redirect('admin_view_dashboard')
        else:
            return redirect('exam')

      else:
        messages.error(request, "Invalid username or password.")
    else:
      messages.error(request, "Invalid username or password.")
  form = AuthenticationForm()
  return render(request = request,template_name = "accounts/login.html",context={"form":form})

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
  user = request.user
  form = ProfileUpdateForm(instance=user)
  change_password_form = CustomPasswordChangeForm(request.user, request.POST)
  return render(request,'profile.html',{"user":user,"form": form,'change_password_form': change_password_form})


@login_required
def profile_update(request,user_id):
    user = ExamUser.objects.get(id = user_id)
    form = ProfileUpdateForm(request.POST or None, request.FILES or None, instance=user)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile updated successfully')
    else:
        messages.warning(request, 'There was an issue in the form')
    return redirect(request.META.get('HTTP_REFERER', '/'))


def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Update session to prevent log out
            messages.success(request, 'Password changed successfully')
    else:
        messages.warning(request, 'There was an issue in the form, try again!!')
    return redirect('profile')