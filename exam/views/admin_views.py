# customadmin/views.py
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.db.models import Count
from django.db.models.functions import ExtractMonth

from datetime import datetime

from exam.decorators import admin_only
from exam.forms import *
from exam.models import *


@login_required
@admin_only
def admin_dashboard(request):
    total_users_count = ExamUser.objects.all().count()
    total_exam_count = Exam.objects.all().count()
    total_courses_count = Courses.objects.all().count()
    active_users_count = ExamUser.objects.all().filter(is_active=True).count()
    dormant_users_count = ExamUser.objects.all().filter(is_active=False).count()

    context = {
        'total_users_count': total_users_count,
        'active_users_count': active_users_count,
        'dormant_users_count': dormant_users_count,
        'total_exam_count': total_exam_count,
        'total_courses_count': total_courses_count,

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
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Course Created Successfully!')
            return redirect('admin_course_list')
    else:
        form = CourseForm()
    return render(request, 'customadmin/course_list.html', {'courses': courses,'form': form})


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

    # Add a count field to each exam instance
    if request.method == 'POST':
            form = ExamForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, f'Exam Created Successfully!')
                return redirect('admin_exam_list')
    else:
            form = ExamForm()

    return render(request, 'customadmin/exam_list.html', {'exams': exams, 'form': form})


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
def question_list(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Questions.objects.filter(exam_id=exam_id)

    return render(request, 'customadmin/question_list.html', {'questions': questions, 'exam': exam, 'exam_id': exam_id})


@login_required
@admin_only
def add_question(request, exam_id):
    exam = get_object_or_404(Exam, id=exam_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = QuestionAnswerFormSet(request.POST, queryset=QuestionAnswers.objects.none())

        if form.is_valid() and formset.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.course = exam.course
            question.save()

            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, f'Question Added Successfully!')
            return redirect('admin_question_list', exam_id=exam_id)
    else:
        form = QuestionForm()
        formset = QuestionAnswerFormSet(queryset=QuestionAnswers.objects.none())

    context = {'form': form, 'formset': formset, 'exam': exam}
    return render(request, 'customadmin/add_question.html', context)

@login_required
@admin_only
def edit_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = QuestionAnswerFormSet(request.POST, instance=question, queryset=question.questionanswers_set.all())

        if form.is_valid() and formset.is_valid():
            question = form.save()

            answers = formset.save(commit=False)
            for answer in answers:
                answer.question = question
                answer.save()
            messages.success(request, f'Question Updated Successfully!')          
            return redirect('admin_question_list', exam_id=question.exam.id)
    else:
        form = QuestionForm(instance=question)
        formset = QuestionAnswerFormSet(instance=question, queryset=question.questionanswers_set.all())

    context = {'form': form, 'formset': formset, 'question': question}
    return render(request, 'customadmin/edit_question.html', context)


@login_required
@admin_only
def delete_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if question:
        question.delete()
        messages.success(request, f'Question Deleted Successfully!') 
        return redirect('admin_question_list', exam_id=question.exam.id)


def check_answer(request, answer_id):
    try:
        selected_answer = QuestionAnswers.objects.get(pk=answer_id)
        is_correct = selected_answer.is_correct
        explanation = selected_answer.question.answer_explanation
    except QuestionAnswers.DoesNotExist:
        is_correct = False
        explanation = "Invalid answer selected."

    result = {
        'result': 'Correct' if is_correct else 'Incorrect',
        'explanation': explanation,
    }

    return JsonResponse(result)

# Notes Views
@login_required
@admin_only
def note_create(request):
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note created successfully!')
            return redirect('admin_notes_list')
    else:
        form = NotesForm()
    return render(request, 'customadmin/notes_form.html', {'form': form})


@login_required
@admin_only
def note_update(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    if request.method == 'POST':
        form = NotesForm(request.POST, request.FILES, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, 'Note updated successfully!')
            return redirect('admin_note_detail', pk=note.pk)
    else:
        form = NotesForm(instance=note)
    return render(request, 'customadmin/edit_note.html', {'note': note ,'form': form})


@login_required
@admin_only
def note_delete(request, note_id):
    note = get_object_or_404(Notes, pk=note_id)
    note.delete()
    messages.success(request, 'Note deleted successfully!')
    return redirect('admin_notes_list')


@login_required
@admin_only
def admin_notes_list(request):
    notes = Notes.objects.all()
    if request.method == 'POST':
        form = NotesForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, f'Notes Created Successfully!')
            return redirect('admin_notes_list')
    else:
        form = NotesForm()

    return render(request, 'customadmin/notes_form.html', {'notes': notes, 'form': form})

def admin_note_detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    return render(request, 'customadmin/note_details.html', {'note': note})


# Graphs Views
# User Signup yearly visualization
def visualize_user_signup(request):
    # Get the year of the current date
    current_year = datetime.now().year

    # Filter users who signed up in the current year
    signups_by_month = ExamUser.objects.filter(date_joined__year=current_year)\
                                   .annotate(month=ExtractMonth('date_joined'))\
                                   .values('month')\
                                   .annotate(count=Count('id'))
    
    # Create a list to hold the counts for each month
    user_signups_data = [0] * 12
    
    # Populate the list with counts for each month
    for signup in signups_by_month:
        month_index = signup['month'] - 1  # Adjust month index (0-based)
        user_signups_data[month_index] = signup['count']
    
    context = {
        'user_signups_data': user_signups_data
    }

    return render(request, 'customadmin/dashboard.html', context)

# Distribution of Courses Based on the Number of Questions
def course_question_distribution(request):
    # Query to get the count of questions for each course
    course_question_counts = Courses.objects.annotate(num_questions=Count('questions'))

    # Extract course names and question counts
    course_names = [course.course_name for course in course_question_counts]
    question_counts = [course.num_questions for course in course_question_counts]

    context = { 
        'course_names': course_names,
        'question_counts': question_counts
    }

    return render(request, 'customadmin/dashboard.html', context)


# Distribution of Exams Based on Durations
def exam_duration_distribution(request):
    # Query to get the count of exams for each duration
    exam_duration_counts = Exam.objects.values('duration').annotate(count=Count('id'))

    # Extract durations and exam counts
    durations = [exam['duration'] for exam in exam_duration_counts]
    exam_counts = [exam['count'] for exam in exam_duration_counts]

    context = {
        'durations': durations,
        'exam_counts': exam_counts,
    }
    return render(request, 'customadmin/dashboard.html', context)
