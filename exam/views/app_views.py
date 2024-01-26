from django.shortcuts import render, get_object_or_404

from exam.models import Exam, Questions, Notes


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


def notes_list(request):
    notes = Notes.objects.all()
    return render(request, 'notes_list.html', {'notes': notes})

def note_detail(request, pk):
    note = get_object_or_404(Notes, pk=pk)
    return render(request, 'note_details.html', {'note': note})
