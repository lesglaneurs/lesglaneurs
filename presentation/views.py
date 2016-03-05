# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404
from .models import Project, Story, UserType, StructureType, Address, User, Event, EventUser, Plant, Area, GleanablePlant, EventPlantGleaned
from django.db import models

from django.utils.datastructures import OrderedDict

# Create your views here.
def home(request):
    return render(request, 'presentation/home.html')

def rebelle(request):
    return render(request, 'presentation/rebelle.html')

def test(request):
    return render(request, 'presentation/test.html')

#
# def bocal_local(request):
#     return render(request, 'presentation/bocal_local.html')

def project(request, project_name):
    project = get_object_or_404(Project, name=project_name)
    #stories = project.objects.get().all()
    #print stories

    identity_items = OrderedDict({
        u'Gérant': project.contact_name,
        'Personnel': project.workers,
        u'Année de création': project.creation_date,
        'Structure': project.structure
    })
    # identity_items = [
    #     (u'Gérant', project.contact_name),
    #     ('Personnel', u"un cuisinier d\'insertion par structure")
    # ]
    ## Not printed in the right order ???
    return render(request, 'presentation/project.html', {'project': project, 'identity_items': identity_items})



## TRY TO MANAGE MANY USERS RELATED TO EVENT
## THEN MANY ORGANIZERS
## THEN ENGLISH FRENCH
class EventView():
    event= Event()
    organizer = User()

def calendar(request):
    events = Event.objects.all()
    event_views = []
    for e in events:
        event_view = EventView()
        event_view.event = e

        event_user = EventUser.objects.get(event=e)
        if event_user.type == UserType.objects.get(name='organisateur'):
            event_view.organizer = User.objects.get(name=event_user.user)

        event_views.append(event_view)
    return render(request, 'presentation/calendar.html', {'event_views': event_views})


def event(request, event_id):
    event = Event.object.get(pk=event_id)

    # retrieve list of users
    event_user = EventUser.object.filter(event=event_id)
    user_list = User.object.filter(id__in=event_user)

    # retrieve list of plants
    epg = EventPlantGleaned.object.filter(event=event_id)
    plant_list = GleanablePlant.object.filter(id__in=epg)

    return render(request, 'presentation/event.html', {'event': event, 'user_list': user_list, 'plant_list': plant_list})
