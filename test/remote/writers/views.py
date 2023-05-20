from django.shortcuts import render

# Create your views here.
def writersdashboard(request):
    return render(request, 'writersdashboard.html')