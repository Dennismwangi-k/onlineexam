from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'landing.html')

def exam(request):
    return render(request, 'exam.html')

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

def test(request):
    return render(request, 'test.html')
