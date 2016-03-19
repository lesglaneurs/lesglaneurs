# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Project, Story, Event
from django.utils.datastructures import OrderedDict

def home(request):
    return render(request, 'presentation/home.html')

def calendar(request):
    events_glan = Event.objects.all()
    return render(request, 'presentation/calendar.html', {'events_glan' : events_glan})

def test(request):
    return render(request, 'presentation/test.html')

def project(request, project_name):
    project = get_object_or_404(Project, name=project_name)
    #stories = project.objects.get().all()

    identity_items = OrderedDict({
        u'Gérant': project.contact_name,
        'Personnel': project.workers,
        u'Année de création': project.creation_date,
        'Structure': project.structure
    })

    event = Event.objects.get(project=project)

    return render(request, 'presentation/project.html',
                  {'project':project,
                   'identity_items':identity_items,
                   'evenement': event
                   })

