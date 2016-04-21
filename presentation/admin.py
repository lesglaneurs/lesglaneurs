from django.contrib import admin
from .models import Project, Story, Event, Address

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)
admin.site.register(Event)
admin.site.register(Address)
