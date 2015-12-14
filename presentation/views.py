from django.shortcuts import render, get_object_or_404
from .models import Project, Story

# Create your views here.


def home(request):
    return render(request, 'presentation/home.html')

def rebelle(request):
    return render(request, 'presentation/rebelle.html')

def bocal_local(request):
    return render(request, 'presentation/bocal_local.html')

def project(request, project_name):
    project = get_object_or_404(Project, name=project_name)
    #stories = project.objects.get().all()
    #print stories
    return render(request, 'presentation/project.html', {'project':project})

