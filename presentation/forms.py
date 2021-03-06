# -*- coding: utf-8 -*-
from django import forms
from .models import Person, Address, Plant, Event, Garden, Project
from django.contrib.auth.models import User, Group



class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class ContactForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = ['firstname', 'lastname', 'email']

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
    name = forms.CharField(label="Titre de l'événement",
                           max_length=100,
                           widget=forms.TextInput(attrs={'value':''}))
    description = forms.CharField(required=False, max_length=512)
    start_date = forms.DateTimeField(label="Date/heure de début",
                                     widget=forms.TextInput(attrs={'class':'datetimepicker'}))
    end_date = forms.CharField(label="Date/heure de fin",
                               widget=forms.TextInput(attrs={'class':'datetimepicker'}))

class GardenForm(forms.ModelForm):
    class Meta:
        model = Garden
        fields = ['surface']


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields =['name', 'web_site']

    def clean(self):
        data = self.cleaned_data
        if User.objects.filter(username=data['name']).exists() or Group.objects.filter(name=data['name']+'_admin'):
            self.add_error('name', 'Un projet avec ce nom existe déjà.')

        return data