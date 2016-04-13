# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Project, Story, Event
from django.utils.datastructures import OrderedDict
from django.http import JsonResponse
from django.core import serializers

def home(request):
    return render(request, 'presentation/home.html')

def map(request):
    return render(request, 'presentation/map.html')

def points(request):
    result = {'points':
              [{'name': "Saint-Pierre d'Aurillac",
                'coords': [44.572329, -0.19046500000001743]},
               {'name': 'Paris',
                'coords': [48.856614, 2.3522219000000177]},
               {'name': 'Guiseniers',
                'coords': [49.21267599999999, 1.4749530000000277]},
              ],
    }
    return JsonResponse(result)

def calendar(request):
    events_glan = Event.objects.all()
    return render(request, 'presentation/calendar.html', {'events_glan' : events_glan})

def test(request):
    return render(request, 'presentation/test.html')

def projects(request, project_id=None):
    if project_id:
        project = get_object_or_404(Project, id=project_id)

        identity_items = OrderedDict({
            u'Gérant': project.contact_name,
            u'Personnel': project.workers,
            u'Année de création': project.creation_date,
            u'Structure': project.structure
        })

        if Event.objects.filter(project=project).exists():
            events = Event.objects.filter(project=project)
        else:
            events = []

        return render(request, 'presentation/project.html',
                      {u'project':project,
                       u'identity_items':identity_items,
                       u'events_glan': events
                       })
    else:
         projects = serializers.serialize("json", Project.objects.all())
         return JsonResponse(projects, safe=False)


def events(request):
    events = Event.objects.all()
    calendar_events = []
    for event in events:
        project = get_object_or_404(Project, name=event.project)
        calendar_events.append(
        {
            'title': event.name,
            'start': event.start_date.date(),
            'end': event.end_date.date(),
            'description': event.description,
            'project_name': project.name,
            'project_logo': project.logo.url,
            #'place': event.place,
            'contact_name': project.contact_name,
            'contact_phone':project.telephone,
            'contact_email':project.email,
            #'inscription': "obligatoire",
            #'event_details_link': event.website,
            'project_site': project.web_site
        })
    return JsonResponse(calendar_events, safe=False)
