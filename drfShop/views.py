from django.shortcuts import render


# Create your views here.

def show_main_page(request):
    return render(request, 'index.html')
