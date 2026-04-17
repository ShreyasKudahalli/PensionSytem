from django.shortcuts import render,HttpResponse

# Create your views here.
def home(request):
    return render(request, 'transperancy_dashboard.html')

def apply_pension(request):
    return render(request, 'apply-pension.html')

def pension_status(request):
    return render(request, 'my-pension-status.html')