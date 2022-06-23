from django.shortcuts import render


# Create your views here.

def show_main_page(request):
    return render(request, 'index.html')

def show_sample_page(request):
    return render(request, 'sample.html')
