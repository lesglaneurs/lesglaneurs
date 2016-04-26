# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)

class Project(models.Model):
    name = models.CharField(null=True,max_length=100, help_text="Le nom du projet")
    owner_image = models.ImageField(null=True, upload_to=user_directory_path, help_text="Photo du chef du projet")
    # creation_date = models.DecimalField(max_digits=8, decimal_places=0, default='9999')
    creation_date = models.PositiveIntegerField(null=True, help_text="date de création")
    contact_name = models.CharField(null=True,max_length=100, help_text="nom du contact de référence")
    email = models.EmailField(null=True, help_text="email de contact")
    # telephone = models.DecimalField(max_digits=10, decimal_places=0, default='0600000000')
    telephone = models.CharField(null=True, max_length=14, help_text="numéro de téléphone")
    web_site = models.URLField(null=True, help_text="site Web du projet")

    structure = models.CharField(null=True,max_length=100, help_text="structure administrative du projet")
    location_today = models.ImageField(null=True, upload_to=user_directory_path, help_text="présence du projet aujourd'hui")
    location_target = models.ImageField(null=True, upload_to=user_directory_path, help_text="prévision d'évolution géographique")
    logo = models.ImageField(null=True, upload_to=user_directory_path, help_text="photo du logo du projet")
    project_structure = models.ImageField(null=True, upload_to=user_directory_path, help_text="image de la strcuture globale du projet")
    workers = models.TextField(null=True, help_text="participants au projet - bénévols, salariés")

    def __unicode__(self):
        return unicode(self.name)


class Story(models.Model):
    description = models.CharField(null=True,max_length=200)
    project = models.ForeignKey(Project)
    content = models.TextField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()

    def __unicode__(self):
        return unicode(self.description)

class Address(models.Model):
    address = models.CharField(max_length=500, null=True, blank=True)
    code = models.CharField(max_length=5)
    city = models.CharField(max_length=100, null=True, blank=True)
    country = models.CharField(max_length=100, default="France")
    latitude = models.DecimalField(decimal_places=15, max_digits=18, blank=True)
    longitude = models.DecimalField(decimal_places=15, max_digits=18, blank=True)

    def __unicode__(self):
        return self.address + ' ' + self.code + ' ' + self.city

class Event(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True, max_length=1000)
    project = models.ForeignKey(Project, null=True)
    addresses = models.ManyToManyField(Address)

    def __unicode__(self):
        return self.name
