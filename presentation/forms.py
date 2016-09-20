# -*- coding: utf-8 -*-
from django import forms
from .models import Person, Address, Plant, Event, Garden

class ContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'email', 'telephone']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'code', 'city']

class PlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'number']
        
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'description', 'project']

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['surface']
