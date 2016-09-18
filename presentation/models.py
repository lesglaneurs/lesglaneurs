# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.gis.db import models as gis_models
from datetime import datetime

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)

class Address(models.Model):

    class Meta:
        verbose_name = 'Adresse'

    address = models.CharField('Adresse',
                               max_length=500,
                               null=True,
                               blank=True)
    code = models.CharField('Code postal', max_length=5)
    city = models.CharField('Ville',
                            max_length=100,
                            null=True,
                            blank=True)
    country = models.CharField('Pays',
                               max_length=100,
                               default='France')
    point = gis_models.PointField('Coordonnées',
                                  null=True,
                                  blank=True)

    def __unicode__(self):
        return self.address + ' ' + self.code + ' ' + self.city
        
class Project(models.Model):
    class Meta: verbose_name = 'Projet'

    name = models.CharField('Nom du projet', max_length=100)
    creation_date = models.DateField('Date de création',
                                     blank=True, null=True)
    contact_name = models.CharField('Nom du contact de référence',
                                    max_length=100,
                                    blank=True, null=True)
    email = models.EmailField('Email de contact',
                              blank=True, null=True)
    telephone = models.CharField('Numéro de téléphone',
                                 max_length=14,
                                 blank=True, null=True)
    web_site = models.URLField('Site web du projet',
                               blank=True, null=True)
    STRUCTURE = (
        ('libre', 'structure libre sans statut officiel'),
        ('asso', 'association loi 1900'), 
        ('sarl', 'SARL'),
    )
    structure = models.CharField(choices=STRUCTURE, max_length=50, default='asso')
    
    logo = models.ImageField('Logo du projet',
                             upload_to=user_directory_path,
                             blank=True, null=True)
    def __unicode__(self):
        return unicode(self.name)

class ProjectProfile(models.Model):
    class Meta: verbose_name = 'Fiche projet'

    project = models.ForeignKey(Project, verbose_name='Project')
    owner_image = models.ImageField('Photo du chef du projet',
                                    upload_to=user_directory_path,
                                    blank=True, null=True)
    location_today = models.ImageField("Présence du projet aujourd'hui",
                                       upload_to=user_directory_path,
                                       blank=True, null=True,)
    location_target = models.ImageField("Prévision d'évolution géographique",
                                        upload_to=user_directory_path,
                                        blank=True, null=True)
    project_structure = models.ImageField('Image de la structure globale du projet',
                                          upload_to=user_directory_path,
                                          blank=True, null=True)
    workers = models.TextField('Participants (bénévoles, salariés)',
                               blank=True, null=True)
    def __unicode__(self):
        return unicode(self.project.name)

class Person(models.Model):

    class Meta:
        verbose_name = 'Personne'

    firstname = models.CharField('Prénom',
                            max_length=128,
                            blank=True,
                            null=True)
    lastname = models.CharField('Nom',
                                max_length=128,
                                blank=True,
                                null=True)
    telephone = models.CharField('Numéro de téléphone',
                                 max_length=14,
                                 blank=True,
                                 null=True)
    mobile = models.CharField('Numéro de téléphone mobile',
                                 max_length=14,
                                 blank=True,
                                 null=True)
    email = models.EmailField('Email de contact',
                              blank=True,
                              null=True)
    address = models.ForeignKey(Address,
                                blank=True,
                                null=True,
                                verbose_name='Adresse')
    projects = models.ManyToManyField(
                Project,
                through='Membership',
                through_fields=('person', 'project', 'membership'),
        )

    def __unicode__(self):
        return unicode(self.firstname) + ' ' + unicode(self.lastname)

class Role(models.Model):
    class Meta: verbose_name = 'Role'

    name = models.CharField('Nom',
                            max_length=128,
                            default='membre',
                            unique=True,
                            help_text="Le role d'une personne pour un projet en particulier - membre par défaut")
    def __unicode__(self):
        return unicode(self.name)

class Membership(models.Model):

    person = models.ForeignKey(Person, verbose_name='Personne')
    project = models.ForeignKey(Project, verbose_name='Projet')
    role = models.ForeignKey(Role, verbose_name='Role')
    def __unicode__(self):
        return unicode(self.person) + ' - ' + unicode(self.role) + ' du projet ' + unicode(self.project)

class Story(models.Model):
    description = models.CharField(null=True,
                                   max_length=200)
    project = models.ForeignKey(Project)
    content = models.TextField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()

    def __unicode__(self):
        return unicode(self.description)

class Event(models.Model):
    class Meta: verbose_name = 'Evénement'

    name = models.CharField(max_length=500)
    start_date = models.DateTimeField('Date de début', default=datetime.now, blank=True)
    end_date = models.DateTimeField('Date de fin', default=datetime.now, blank=True)
    description = models.TextField(blank=True,
                                   null=True,
                                   max_length=1000)
    project = models.ForeignKey(Project, verbose_name='Organisateur')
    addresses = models.ManyToManyField(Address, verbose_name='Adresse', 
                                       blank=True)

    def __unicode__(self):
        return self.name

class Garden(models.Model):

    class Meta:
        verbose_name = 'Terrain'

    surface = models.PositiveIntegerField('Surface (m2)',
                                          blank=True,
                                          null=True)
    person = models.ForeignKey(Person)
    address = models.ForeignKey(Address,
                                verbose_name='Adresse')

    def __unicode__(self):
        return u'terrain de ' + unicode(self.person.firstname) + u' au ' + unicode(self.address.address)

class PlantSpecies(models.Model):

    class Meta:
        verbose_name = 'Espece'

    name = models.CharField(u'Nom commun de la plante',
                            max_length=100)
    harvest_start_date = models.DateField(u'Date de début de récolte minimum',
                                          blank=True,
                                          null=True)
    harvest_end_date = models.DateField(u'Date de fin de récolte maximum',
                                        blank=True,
                                        null=True)

    def __unicode__(self):
        return u'{} (récolte du {} au {})'.format(
            self.name,
            self.harvest_start_date.strftime("%d/%m"),
            self.harvest_end_date.strftime("%d/%m"))

class Plant(models.Model):

    class Meta:
        verbose_name = 'Plante d un jardin'

    name = models.ForeignKey(PlantSpecies,
                             verbose_name='Nom')
    garden = models.ForeignKey(Garden,
                               verbose_name='Terrain',
                               null=True)
    number = models.IntegerField(u'nombre de pieds',
                                 blank=True,
                                 null=True)
    harvest_start_date = models.DateField(
        u'Date estimée de début de récolte sur ce terrain',
        blank=True,
        null=True)
    harvest_end_date = models.DateField(
        u'Date estimée de fin de récolte sur ce terrain',
        blank=True,
        null=True)

    def __unicode__(self):
        return u'{} du {})'.format(
            self.name,
            self.garden)

