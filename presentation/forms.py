# -*- coding: utf-8 -*-
from django import forms
from .models import Event

class ContactForm(forms.Form):
    name = forms.CharField(label='Prénom', max_length=100)
    surname = forms.CharField(label='Nom', max_length=100)
    email = forms.CharField(label='Email', max_length=100)
    telephone = forms.CharField(label='Téléphone', max_length=14)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'description', 'project']
            
# How to add popup in contact.html with Javascript form which works in table.html but does not updated Django Database
# http://www.abidibo.net/blog/2014/05/26/how-implement-modal-popup-django-forms-bootstrap/
# Use Django Media Elements
# https://docs.djangoproject.com/en/1.9/topics/forms/media/#media-as-a-dynamic-property
