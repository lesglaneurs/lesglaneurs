# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Project, Story
from django.utils.datastructures import OrderedDict

# Create your views here.
def home(request):
    return render(request, 'presentation/home.html')

# def rebelle(request):
#     return render(request, 'presentation/rebelle.html')
#
# def bocal_local(request):
#     return render(request, 'presentation/bocal_local.html')

def project(request, project_name):
    project = get_object_or_404(Project, name=project_name)
    #stories = project.objects.get().all()
    #print stories

    identity_items = OrderedDict({
        u'Gérant':project.contact_name,
        'Personnel':u"un cuisinier d\'insertion par structure",
        u'Année de création':project.creation_date,
        'Site internet':project.web_site,
        'Email':project.email
    })
    # identity_items = [
    #     (u'Gérant', project.contact_name),
    #     ('Personnel', u"un cuisinier d\'insertion par structure")
    # ]
    ## Not printed in the right order ???
    print identity_items
    return render(request, 'presentation/project.html', {'project':project, 'identity_items':identity_items})

