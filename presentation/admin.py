from django.contrib import admin
from .models import Project, Story, Person, Role, Membership, Event, Address, Garden

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)
admin.site.register(Role)
admin.site.register(Membership)
admin.site.register(Event)
admin.site.register(Address)

class GardenAdmin(admin.TabularInline):

    extra = 1
    model = Garden

class PersonAdmin(admin.ModelAdmin):

    model = Person
    inlines = [GardenAdmin]

admin.site.register(Person, PersonAdmin)
