from django.contrib import admin
from nested_inline.admin import NestedTabularInline, NestedModelAdmin

from .models import (Address,
                     Event,
                     Garden,
                     Membership,
                     Person,
                     Plant,
                     Project,
                     Role,
                     Story,
                 )

# Register your models here.
admin.site.register(Address)
admin.site.register(Event)
admin.site.register(Membership)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Story)


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
