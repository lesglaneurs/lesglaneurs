from django.contrib import admin
from .models import Project, Story, Event, Address, EventAddress

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)
admin.site.register(Event)
admin.site.register(Address)
admin.site.register(EventAddress)