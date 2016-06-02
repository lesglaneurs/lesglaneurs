from django.contrib import admin

from leaflet.admin import LeafletGeoAdmin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from .models import (Address,
                     Event,
                     Garden,
                     Membership,
                     Person,
                     Plant,
                     PlantSpecies,
                     Project,
                     Role,
                     Story,
                 )

# Register your models here.
admin.site.register(Event)
admin.site.register(Membership)
admin.site.register(PlantSpecies)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Story)

class AddressAdmin(LeafletGeoAdmin):
    class Media:
        js = ['presentation/js/address.js']

admin.site.register(Address, AddressAdmin)

class PlantAdmin(NestedTabularInline):

    extra = 1
    model = Plant

class GardenAdmin(NestedTabularInline):

    extra = 1
    model = Garden
    inlines = [PlantAdmin]

class PersonAdmin(NestedModelAdmin):

    model = Person
    inlines = [GardenAdmin]

admin.site.register(Person, PersonAdmin)
