from django.contrib import admin
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
admin.site.register(Plant)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Story)


class GardenAdmin(admin.TabularInline):

    extra = 1
    model = Garden

class PersonAdmin(admin.ModelAdmin):

    model = Person
    inlines = [GardenAdmin]

admin.site.register(Person, PersonAdmin)
