from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from exam.models import ExamUser

class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=144, required=True)
    last_name = forms.CharField(max_length=144, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=13, required=True)
    username = forms.CharField(max_length=150, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput, required=True)

    class Meta:
        model =ExamUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'username', 'password1', 'password2']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =ExamUser
        fields = ['first_name', 'last_name', 'email', 'phone','profile_picture']


class AdminProfileUpdateForm(forms.ModelForm):
    class Meta:
        model =ExamUser
        fields = ['first_name', 'last_name', 'email', 'username', 'phone','is_active']

class CustomPasswordChangeForm(PasswordChangeForm):
    class Meta:
        model =ExamUser 
        fields = ['old_password', 'new_password1', 'new_password2']


class AdminSetPasswordForm(forms.ModelForm):
    new_password1 = forms.CharField(label='New Password', widget=forms.PasswordInput)
    new_password2 = forms.CharField(label='Confirm New Password', widget=forms.PasswordInput)

    class Meta:
        model = ExamUser
        fields = []

    def clean(self):
        cleaned_data = super().clean()
        new_password1 = cleaned_data.get('new_password1')
        new_password2 = cleaned_data.get('new_password2')

        if new_password1 and new_password1 != new_password2:
            self.add_error('new_password2', "The two password fields didn't match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["new_password1"])
        if commit:
            user.save()
        return user