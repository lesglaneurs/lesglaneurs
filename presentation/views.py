# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import csv
from itertools import izip
import json
import os

from django import forms
from django.conf import settings
from django.contrib.gis.geos import GEOSGeometry
from django.core import serializers
from django.db.models import Q
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.utils.datastructures import OrderedDict
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate, login

from .models import Address, Project, Story, Event, Person, Membership, Role, Garden, Plant, PlantSpecies
from .forms import ContactForm, AddressForm, PlantForm, EventForm, GardenForm, ProjectForm, UserForm

## Global functions
def jsonify(objects):
    if hasattr(objects, '__iter__'):
        return json.loads(serializers.serialize('json', objects))
    else:
        [result] = json.loads(serializers.serialize('json', [objects]))
        return result

## Get data for map filters
def get_persons():
    persons = Person.objects.order_by('firstname').values('firstname').distinct()
    return ['Tous'] + [person['firstname'] for person in persons]

def get_memberships():
    memberships = Membership.objects.order_by('person').distinct()
    return ['Tous'] + sorted([membership.__str__() for membership in memberships])

def get_gardens():
    [gardens] = Garden.objects.all(),
    return ['Tous'] + ['jardin de ' + unicode(garden.person.firstname)
                       for garden in gardens]

def get_plants():
    [plants] = PlantSpecies.objects.all(),
    return ['Tous'] + [unicode(plant.name)
                       for plant in plants]

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

## render
def home(request):
    return render(request, 'presentation/home.html')

def map(request):
    return render(request, 'presentation/map.html',
                  {'projects': get_projects(),
                   'departments': get_departments(),
                   'months': get_months()})

def map_plants(request):
    return render(request, 'presentation/map_plants.html',
                  {'plants': get_plants(),
                   'gardens': get_gardens(),
                   'persons': get_persons()})

def map_gardens(request):
    return render(request, 'presentation/map_gardens.html',
                  {'gardens': get_gardens(),
                   'persons': get_persons()})

## DB operations
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

    addresses_records = [Address(address=address['address'],
                                 code=address['code'],
                                 city=address['city'],
                                 point=GEOSGeometry('POINT({lon} {lat})'.format(
                                     lon=address['coords'][1],
                                     lat=address['coords'][0])
                                                )
                             )
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

    persons_records = [Person(firstname=first_name, lastname="Dutronc")
                       for first_name in [u'Aurelie', 'Bernard', 'Camille']]
    [person_record.save() for person_record in persons_records]

    role_contact, created = Role.objects.get_or_create(name='contact')

    membership_records = [Membership(person=person, project=project, role=role_contact)
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
    events_details = []
    for event in events:
        project_contacts = Membership.objects.filter(project__name__exact=event.project, role__name__exact='contact')
        contact_name = "nom du contact indisponible"
        if project_contacts:
            contact_name = project_contacts[0].person.firstname + ' ' + project_contacts[0].person.lastname
        events_details.append({'name': event.name,
                               'start_date': event.start_date,
                               'end_date': event.end_date,
                               'contact': contact_name,
                               'addresses': jsonify(event.addresses.all()),
                               'project': jsonify(event.project)})
    return JsonResponse({'events': events_details})

## JSON data
def gardens(request):
    gardens_details = []
    for garden in Garden.objects.all():
        gardens_details.append({
            'person':  jsonify(Person.objects.get(pk= garden.person.id))['fields'],
            'address': jsonify(Address.objects.get(pk=garden.address.id))['fields'],
            'surface': garden.surface}),
    return JsonResponse({'gardens': gardens_details})

def garden_details(garden):
    garden_details = {'person':  jsonify(Person.objects.get(pk= garden.person.id))['fields'],
                      'address': jsonify(Address.objects.get(pk=garden.address.id))['fields'],
                      'surface': garden.surface},
    return garden_details

def plants(request):
    plants = []
    for plant in Plant.objects.all():
        plants.append({
            'name': jsonify(PlantSpecies.objects.get(pk = plant.name.id))['fields']['name'],
            'garden': garden_details(Garden.objects.get(pk = plant.garden.id))
        }),
    return JsonResponse({'plants': plants})

def plants_info(request):
    plants = Plant.objects.all()
    plant = request.GET.get('plant')
    if plant:
        plant_name = PlantSpecies.objects.get(name = plant)
        plants = plants.filter(name = plant_name)
    plants_details = []
    for plant in plants:
        plants_details.append({
            'name': jsonify(PlantSpecies.objects.get(pk = plant.name.id))['fields']['name'],
            'garden': garden_details(Garden.objects.get(pk = plant.garden.id))
        }),
    return JsonResponse({'plants': plants_details})

def map_addresses(request):
    return JsonResponse({'addresses': jsonify(Address.objects.all())})

def persons(request):
    return JsonResponse({'persons': jsonify(Person.objects.all())})

def calendar(request):
    events_glan = Event.objects.all()
    return render(request, 'presentation/calendar.html', {'events_glan' : events_glan})

def wireframe(request):
    return render(request, 'presentation/wireframe.html')

def event_add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        project_list = Project.objects.filter(admin_group__in = request.user.groups.all())

        form = EventForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            event = Event(name = data['name'],
                          start_date = data['start_date'],
                          end_date = data['end_date'],
                          description = data['description'],
                          project = data['project']
            )
            event.save()
            return HttpResponseRedirect('/local/presentation/calendar')
        else:
            return HttpResponseRedirect('/local/presentation/event_add')
    else:
        form = EventForm()
    return render(request, 'presentation/calendar.html', {'form': form,
                                                          'events': Event.objects.all(),
                                                          'persons': Person.objects.all()})


def contact_add(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        form_address = AddressForm(request.POST)
        form_plant = PlantForm(request.POST)
        form_garden = GardenForm(request.POST)

        if form.is_valid():
            # address form can be invalid or empty  < to be enhanced
            if not form_address.is_valid():
                address = None
            else:
                data_address = form_address.cleaned_data

                address = Address(address=data_address['address'],
                                  city=data_address['city'],
                                  code=data_address['code'])
                address.save()

            data_person = form.cleaned_data

            # phone can be empty
            if 'telephone' not in data_person:
                data_person['telephone'] = None

            # save contact
            person = Person(firstname=data_person['firstname'],
                            lastname=data_person['lastname'],
                            email=data_person['email'],
                            telephone=data_person['telephone'],
                            )
            person.save()

            # add membership to new contact
            project_list = Project.objects.filter(admin_group__in=request.user.groups.all())
            role = Role.objects.get_or_create(name='membre')[0]
            membership = Membership(person=person, project=project_list[0], role=role)
            membership.save()

            if form_plant.is_valid() and form_garden.is_valid():

                data_garden = form_garden.cleaned_data
                garden = Garden(surface=data_garden['surface'],
                                person=Person.objects.get(pk=person.id),
                                address=Address.objects.get(pk=address.id))
                garden.save()

                data_plant = form_plant.cleaned_data
                plant = Plant(name=data_plant['name'],
                              number=data_plant['number'],
                              garden=Garden.objects.get(pk=garden.id))
                plant.save()

            return HttpResponseRedirect('/local/presentation/contacts')
        else:
            return HttpResponseRedirect('/local/presentation/contact_add')
    else:
        form = ContactForm()
        form_address = AddressForm()
        form_plant = PlantForm()
        form_garden = GardenForm()
    return render(request, 'presentation/contact_add.html', {'form': form,
                                                             'form_address': form_address,
                                                             'form_plant': form_plant,
                                                             'form_garden': form_garden,
                                                             'plants': Plant.objects.all(),
                                                             'persons': Person.objects.all()})


def contacts(request):
    # user > group > project > contacts
    project_list = Project.objects.filter(admin_group__in=request.user.groups.all())
    person_list = Person.objects.filter(projects__in=project_list)
    return render(request, 'presentation/contact.html', {'persons': person_list})


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

    project_list = Project.objects.filter(admin_group__in = request.user.groups.all())
    events = Event.objects.filter(project__in = project_list)

    calendar_events = []
    for event in events:
        project = get_object_or_404(Project, name=event.project)
        if hasattr(project.logo, 'url'): 
            logo = project.logo.url
        else:
            logo = ''

        calendar_events.append(
            {
            'title': event.name,
                'start': event.start_date.date(),
                'end': event.end_date.date(),
                'description': event.description,
                'project_name': project.name,
                'project_logo': logo,
                #'place': event.place,
                'contact_name': project.contact_name,
                'contact_phone':project.telephone,
                'contact_email':project.email,
                #'inscription': "obligatoire",
                #'event_details_link': event.website,
                'project_site': project.web_site
            })
    return JsonResponse(calendar_events, safe=False)


def contact_clean():

    # clean persons not in any project
    contact_in_membership = Membership.objects.all().values_list('person', flat=True)
    for p in Person.objects.exclude(id__in=contact_in_membership):
        p.delete()

    # clean users not super admin and not linked to any person
    user_in_contact = Person.objects.exclude(user = None).values_list('user', flat=True)
    for u in User.objects.filter(is_superuser=False).exclude(id__in=user_in_contact):
        u.delete()

    # clean empty groups
    group_empty = User.objects.exclude(groups=None).values_list('groups', flat=True)
    for g in Group.objects.exclude(id__in=group_empty):
        g.delete()



def project_add(request):
    contact_clean()

    if request.method == 'POST':
        project_form = ProjectForm(request.POST)
        contact_form = ContactForm(request.POST)
        user_form = UserForm(request.POST)

        if project_form.is_valid() and contact_form.is_valid() and user_form.is_valid():

            # project
            project_form.clean()
            project_data = project_form.cleaned_data

            project_group = Group()
            project_group.name = project_data['name']+'_admin'
            project_group.save()
            project = Project(name = project_data['name'],
                              web_site = project_data['web_site'],
                              admin_group = project_group)

            # user
            user_data = user_form.cleaned_data

            # if User.objects.filter(username=user_data['username']).exists():
            #     raise forms.ValidationError(u'Username "%s" is already in use.' % user_data['username'])
            # else:
            user = User.objects.create_user(username=user_data['username'],
                                            password = user_data['password'])

            project_group.user_set.add(user)

            # contact
            contact_data = contact_form.cleaned_data

            # if Person.objects.filter(email=contact_data['email']).exists():
            #     raise forms.ValidationError(u'Username "%s" is already in use.' % user_data['username'])
            # else:
            contact = Person(firstname = contact_data['firstname'],
                             lastname = contact_data['lastname'],
                             email = contact_data['email'],
                             #telephone = contact_data['telephone'],
                             user = user)
            contact.save()
            project.save()

            # add membership to new contact
            role = Role.objects.get_or_create(name='admin')[0]
            Membership(person=contact, project=project, role=role).save()

            # automatically login
            user = authenticate(username=user_data['username'],
                                password = user_data['password'])
            login(request, user)
            return HttpResponseRedirect("wireframe/")
    else:
        user_form = UserForm()
        project_form = ProjectForm()
        contact_form = ContactForm()

    return render(request, 'presentation/project_add.html', {'project_form': project_form, 'contact_form': contact_form, 'user_form': user_form})