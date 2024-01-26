from django.shortcuts import render

from exam.models import Exam, Questions


# Create your views here.
def index(request):
    return render(request, 'index.html')

def exam(request):
    exams = Exam.objects.all()
    context = {
        "exams": exams,
    }
    return render(request, 'exam.html',context)

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def contact(request):
    return render(request, 'contact.html')

def services(request):
    return render(request, 'service.html')

def blog(request):
    return render(request, 'blog.html')

def test(request,exam_id):
    questions = Questions.objects.filter(exam_id=exam_id)
    context = {
                'questions': questions,
                "exam_id":exam_id
              }
    return render(request, 'test.html', context)
