# -*- coding: utf-8 -*-
from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)

class Project(models.Model):
    name = models.CharField(max_length=100, help_text="Le nom du projet")
    owner_image = models.ImageField(upload_to=user_directory_path,
                                    blank=True, null=True, help_text="Photo du chef du projet")
    creation_date = models.PositiveIntegerField(blank=True, null=True, help_text="date de création")
    contact_name = models.CharField(max_length=100,
                                    blank=True, null=True, help_text="nom du contact de référence")
    email = models.EmailField(blank=True, null=True, help_text="email de contact")
    # telephone = models.DecimalField(max_digits=10, decimal_places=0, default='0600000000')
    telephone = models.CharField(max_length=14, blank=True, null=True, help_text="numéro de téléphone")
    web_site = models.URLField(blank=True, null=True, help_text="site Web du projet")

    structure = models.CharField(max_length=100,
                                 blank=True, null=True, help_text="structure administrative du projet")
    location_today = models.ImageField(upload_to=user_directory_path,
                                       blank=True, null=True, help_text="présence du projet aujourd'hui")
    location_target = models.ImageField(upload_to=user_directory_path,
                                        blank=True, null=True, help_text="prévision d'évolution géographique")
    logo = models.ImageField(upload_to=user_directory_path,
                             blank=True, null=True, help_text="photo du logo du projet")
    project_structure = models.ImageField(upload_to=user_directory_path,
                                          blank=True, null=True, help_text="image de la structure globale du projet")
    workers = models.TextField(blank=True, null=True, help_text="participants au projet - bénévols, salariés")

    def __unicode__(self):
        return unicode(self.name)

class Person(models.Model):
    name = models.CharField(max_length=128, help_text="Le prénom de la personne")
    surname = models.CharField(max_length=128, help_text="Le nom de la personne")
    projects = models.ManyToManyField(
                Project,
                through='Membership',
                through_fields=('person', 'project', 'membership'),
        )

    def __unicode__(self):
        return unicode(self.name) + ' ' + unicode(self.surname)

class Role(models.Model):
    name = models.CharField(max_length=128, default="membre", unique=True,
                             help_text="Le role d'une personne pour un projet en particulier - membre par défaut")
    def __unicode__(self):
        return unicode(self.name)

class Membership(models.Model):
    person = models.ForeignKey(Person)
    project = models.ForeignKey(Project)
    role = models.ForeignKey(Role)
    def __unicode__(self):
        return unicode(self.person) + " - " + unicode(self.role) + " du projet " + unicode(self.project)

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
    code = models.CharField(max_length=5, help_text="code postal")
    city = models.CharField(max_length=100, null=True, blank=True, help_text="ville")
    country = models.CharField(max_length=100, default="France", help_text="pays")
    latitude = models.DecimalField(decimal_places=15, max_digits=18,
                                   blank=True, null=True)
    longitude = models.DecimalField(decimal_places=15, max_digits=18,
                                    blank=True, null=True)

    def __unicode__(self):
        return self.address + ' ' + self.code + ' ' + self.city

class Event(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateTimeField(help_text="date de début")
    end_date = models.DateTimeField(help_text="date de fin")
    description = models.TextField(null=True, max_length=1000)
    project = models.ForeignKey(Project, null=True)
    addresses = models.ManyToManyField(Address)

    def __unicode__(self):
        return self.name
