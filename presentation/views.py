# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from itertools import izip
import json
import os

from django.conf import settings
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.datastructures import OrderedDict

from .models import Address, Project, Story, Event, Person, Membership, Role

def jsonify(objects):
    if hasattr(objects, '__iter__'):
        return json.loads(serializers.serialize('json', objects))
    else:
        [result] = json.loads(serializers.serialize('json', [objects]))
        return result

def get_persons():
    persons = Person.objects.order_by('name').values('name').distinct()
    return ['Tous'] + [person['name'] for person in persons]

def get_memberships():
    memberships = Membership.objects.order_by('person').distinct()
    return ['Tous'] + sorted([membership.__str__() for membership in memberships])

def get_departments():
    select = {'department': "SUBSTR(code, 1, 2)"}
    departments = Address.objects.extra(select=select)
    departments = departments.order_by('department')
    departments = departments.values('department').distinct()
    return ['Tous'] + sorted([department['department'] for department in departments])

def get_projects():
    projects = Project.objects.order_by('name').values('name').distinct()
    return ['Tous'] + sorted([project['name'] for project in projects])

def get_months():
    return ['Tous'] + range(1, 13)

def home(request):
    return render(request, 'presentation/home.html')

def map(request):
    return render(request, 'presentation/map.html',
                  {'projects': get_projects(),
                   'departments': get_departments(),
                   'months': get_months()})

def empty_db(request):
    [object_name.objects.all().delete()
     for object_name in
     [Person, Project, Role, Membership, Address, Event]]
    return HttpResponse()

def load_small_data(request):
    addresses = [{'address': u'34, rue Jules Pedron',
                  'city': u'Guiseniers',
                  'code': u'27700',
                  'coords': [49.21267599999999, 1.4749530000000277]},
                 {'address': u'72, rue de Rennes',
                  'city': u'Paris',
                  'code': u'75006',
                  'coords': [48.856614, 2.3522219000000177]},
                 {'address': u'11 lot des noisetiers',
                  'city': u"Saint-Pierre d'Aurillac",
                  'code': u'33490',
                  'coords': [44.572329, -0.19046500000001743]},

    ]
    return populate_db(addresses)

def load_big_data(request):
    addresses = []
    path = os.path.join(settings.STATIC_ROOT, 'villes_france.csv')
    with open(path) as csvfile:
        reader = csv.reader(csvfile)
        departments = []
        for row in reader:
            department = row[1]
            if department not in departments:
                departments.append(department)
                address = {'address': '1, Place de la Mairie',
                           'city': row[5].decode('utf-8'),
                           'code': row[10],
                           'coords': [float(row[20].replace(',', '.')),
                                      float(row[19].replace(',', '.'))]}
                addresses.append(address)

    return populate_db(addresses)

def populate_db(addresses):

    empty_db(None)

    addresses_records =  [Address(address=address['address'],
                                  code=address['code'],
                                  city=address['city'],
                                  latitude=address['coords'][0],
                                  longitude=address['coords'][1])
                          for address in addresses]

    now = timezone.now()
    events_records = [Event(name=u'Evènement à {}'.format(address['city']),
                            start_date=now,
                            end_date=now) for address in addresses]
    projects_records = [Project(name=u'Association de {}'.format(address['city']))
                        for address in addresses]

    for index, (project_record, address_record, event_record) in \
        enumerate(izip(projects_records, addresses_records, events_records)):
        project_record.save()
        address_record.save()
        event_record.project = project_record
        event_record.save()
        event_record.addresses.add(address_record)
        event_record.save()
        print 'Creating item #{} in the database'.format(index)

    persons_records = [Person(name=first_name, surname="Dutronc")
                        for first_name in [u'Aurelie', 'Bernard', 'Camille']]
    [person_record.save() for person_record in persons_records]

    role_member, created = Role.objects.get_or_create(name='membre')

    membership_records = [Membership(person=person, project=project, role=role_member)
                        for (project, person) in zip(projects_records, persons_records)]
    [membership_record.save() for membership_record in membership_records]

    return HttpResponse()

def map_events(request):
    month = request.GET.get('month')
    project = request.GET.get('project')
    department = request.GET.get('department')
    events = Event.objects.all()
    if project:
        events = events.filter(project__name__exact=project)
    if department:
        events = events.filter(addresses__code__startswith=department)
    if month:
        events = events.filter(Q(start_date__month=month) | Q(end_date__month=month))
    events = [{'name': event.name,
               'start_date': event.start_date,
               'end_date': event.end_date,
               'addresses': jsonify(event.addresses.all()),
               'project': jsonify(event.project)}
              for event in events]
    return JsonResponse({'events': events})

def map_addresses(request):
    return JsonResponse({'addresses': jsonify(Address.objects.all())})

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
