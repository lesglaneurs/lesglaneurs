from django.contrib import admin
from .models import Project, Story, UserType, StructureType, Address, User, Event, EventUser, Plant, Area, GleanablePlant, EventPlantGleaned

# Register your models here.
admin.site.register(Project)
admin.site.register(Story)


admin.site.register(UserType)
admin.site.register(StructureType)
admin.site.register(Address)
admin.site.register(User)
admin.site.register(Event)
admin.site.register(EventUser)
admin.site.register(Plant)
admin.site.register(Area)
admin.site.register(GleanablePlant)
admin.site.register(EventPlantGleaned)