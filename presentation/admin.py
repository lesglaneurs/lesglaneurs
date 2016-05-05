from django.contrib import admin
from .models import Project, Story, Person, Role, Membership, Event, Address

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)
admin.site.register(Person)
admin.site.register(Role)
admin.site.register(Membership)
admin.site.register(Event)
admin.site.register(Address)


