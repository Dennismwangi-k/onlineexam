# customadmin/views.py
from django.shortcuts import render, redirect, get_object_or_404
from exam.models import ExamUser, Questions

def admin_dashboard(request):
    users = ExamUser.objects.all()
    questions = Questions.objects.all()
    context = {'users': users, 'questions': questions}
    return render(request, 'customadmin/dashboard.html', context)

def add_question(request):
    if request.method == 'POST':
        pass
    return render(request, 'customadmin/add_question.html')

def edit_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if request.method == 'POST':
        pass
    context = {'question': question}
    return render(request, 'customadmin/edit_question.html', context)

def delete_question(request, question_id):
    question = get_object_or_404(Questions, pk=question_id)
    if question:
        question.delete()
        return redirect('admin_dashboard')
    context = {'question': question}
    return render(request, 'customadmin/delete_question.html', context)

def view_users(request):
    users = ExamUser.objects.all()
    context = {'users': users}
    return render(request, 'customadmin/view_users.html', context)


def delete_user(request, user_id):
    user = get_object_or_404(ExamUser, pk=user_id)
    if user:
        user.delete()
        return redirect('admin_dashboard')
    context = {'user': user}
    return render(request, 'customadmin/delete_user.html', context)
