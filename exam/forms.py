from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.forms import UserCreationForm
from exam.models import Courses, Exam, ExamUser, QuestionAnswers, Questions

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

class ExamForm(forms.ModelForm):
    class Meta:
        model = Exam
        fields = '__all__'

class CourseForm(forms.ModelForm):
    class Meta:
        model = Courses
        fields = '__all__'

class AnswerForm(forms.ModelForm):
    is_correct = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        label='Mark as Correct Answer'
    )

    class Meta:
        model = QuestionAnswers
        fields = ['answer_text', 'is_correct']
        labels = {
            'answer_text': 'Answer Text',
        }
        widgets = {
            'answer_text': forms.TextInput(attrs={'class': 'form-control'}),
        }


class QuestionAnswerFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        correct_count = 0
        for form in self.forms:
            if form.cleaned_data.get('is_correct'):
                correct_count += 1

        if correct_count != 1:
            raise forms.ValidationError('Exactly one answer should be marked as correct.')

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Questions
        fields = ['question_text','question_type', 'answer_explanation']

QuestionAnswerFormSet = forms.inlineformset_factory(
    Questions,
    QuestionAnswers,
    form=AnswerForm,  # You should create an AnswerForm if not already done
    formset=QuestionAnswerFormSet,
    extra=4,  # Number of answer forms
    min_num=4,
    validate_min=True,
    max_num=4,
    validate_max=True,
)
