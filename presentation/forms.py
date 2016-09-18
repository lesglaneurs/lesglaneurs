# -*- coding: utf-8 -*-
from django import forms
from .models import Person, Address, Event

class ContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'email', 'telephone']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address', 'code', 'city']

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'start_date', 'end_date', 'description', 'project']
