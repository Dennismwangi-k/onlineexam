# customadmin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from exam.models import Courses, Exam, ExamUser, QuestionAnswers, Questions

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from exam.forms import AdminProfileUpdateForm, AdminSetPasswordForm, AnswerForm, CourseForm, ExamForm,ProfileUpdateForm, QuestionAnswerFormSet, QuestionForm
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
    active_users_count = ExamUser.objects.all().filter(is_active=True).count()
    dormant_users_count = ExamUser.objects.all().filter(is_active=False).count()

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
  return render(request, 'customadmin/update_user.html', context)

@login_required
@admin_only
def course_list(request):
    courses = Courses.objects.all()
    return render(request, 'customadmin/course_list.html', {'courses': courses})

@login_required
@admin_only
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course Created Successfully!')
            return redirect('admin_course_list')
    else:
        form = CourseForm()
    return render(request, 'customadmin/add_course.html', {'form': form})

@login_required
@admin_only
def edit_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course Updated Successfully!')
            return redirect('admin_course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'customadmin/edit_course.html', {'form': form, 'course': course})

@login_required
@admin_only
def delete_course(request, course_id):
    course = Courses.objects.get(id=course_id)
    if course:
        course.delete()
        messages.success(request, f'Course deleted!')
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_only
def exam_list(request):
    exams = Exam.objects.all()
    return render(request, 'customadmin/exam_list.html', {'exams': exams})

@login_required
@admin_only
def add_exam(request):
    if request.method == 'POST':
        form = ExamForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exam Created Successfully!')
            return redirect('admin_exam_list')
    else:
        form = ExamForm()
    return render(request, 'customadmin/add_exam.html', {'form': form})

@login_required
@admin_only
def edit_exam(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        form = ExamForm(request.POST, instance=exam)
        if form.is_valid():
            form.save()
            messages.success(request, f'Exam Updated Successfully!')
            return redirect('admin_exam_list')
    else:
        form = ExamForm(instance=exam)
    
    return render(request, 'customadmin/edit_exam.html', {'form': form, 'exam': exam})

@login_required
@admin_only
def delete_exam(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if exam:
        exam.delete()
        messages.success(request, f'Exam deleted!')
        return redirect(request.META.get('HTTP_REFERER', '/'))


@login_required
@admin_only
def question_list(request):
    questions = Questions.objects.all()
    return render(request, 'customadmin/question_list.html', {'questions': questions})

@login_required
@admin_only
def add_question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = QuestionAnswerFormSet(request.POST, queryset=QuestionAnswers.objects.none())

        if form.is_valid() and formset.is_valid():
            question = form.save()
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question_id = question
                answer.save()

            return redirect('question_list')
    else:
        form = QuestionForm()
        formset = QuestionAnswerFormSet(queryset=QuestionAnswers.objects.none())

    context = {'form': form, 'formset': formset}
    return render(request, 'customadmin/add_question.html', context)

@login_required
@admin_only
def edit_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = QuestionAnswerFormSet(request.POST, queryset=question.questionanswers_set.all())

        if form.is_valid() and formset.is_valid():
            question = form.save()
            answers = formset.save(commit=False)
            for answer in answers:
                answer.question_id = question
                answer.save()

            return redirect('question_list')
    else:
        form = QuestionForm(instance=question)
        formset = QuestionAnswerFormSet(queryset=question.questionanswers_set.all())

    context = {'form': form, 'formset': formset, 'question': question}
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