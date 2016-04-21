# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from itertools import izip
import json

from django.core import serializers
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.datastructures import OrderedDict

from .models import Address, Project, Story, Event

def home(request):
    return render(request, 'presentation/home.html')

def map(request):
    return render(request, 'presentation/map.html')

def populate(request):

    Project.objects.all().delete()
    projects = [u'Association de Guiseniers',
                u"Association de Saint-Pierre d'Aurillac",
                u'Association de Paris',
    ]
    projects_records = [Project(name=project) for project in projects]

    addresses = [{'address': u'34, rue Jules Pedron',
                  'city': u'Guiseniers',
                  'code': u'27700',
                  'coords': [49.21267599999999, 1.4749530000000277]},
                 {'address': u'11 lot des noisetiers',
                  'city': u"Saint-Pierre d'Aurillac",
                  'code': u'33490',
                  'coords': [44.572329, -0.19046500000001743]},
                 {'address': u'72, rue de Rennes',
                  'city': u'Paris',
                  'code': u'75006',
                  'coords': [48.856614, 2.3522219000000177]},
    ]

    addresses_records =  [Address(address=address['address'],
                                  code=address['code'],
                                  city=address['city'],
                                  latitude=address['coords'][0],
                                  longitude=address['coords'][1])
                          for address in addresses]

    now = timezone.now()
    events = [u'Evènement à Guinesiers',
              u"Evènement à Saint-Pierre d'Aurillac",
              u'Evènement à Paris',
    ]
    events_records = [Event(name=event,
                            start_date=now,
                            end_date=now) for event in events]

    Address.objects.all().delete()
    Event.objects.all().delete()
    for project_record, address_record, event_record in \
        izip(projects_records, addresses_records, events_records):
        project_record.save()
        address_record.save()
        event_record.project = project_record
        event_record.save()
        address_record.events.add(event_record)
        address_record.save()

    return HttpResponse()

def addresses(request):
    output = serializers.serialize("json", Address.objects.all())
    output = {'addresses': json.loads(output)}
    return JsonResponse(output)

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
