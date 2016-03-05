from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)


#########################################################################


class UserType(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class StructureType(models.Model):
    name = models.CharField(max_length=100)
    def __unicode__(self):
        return self.name

class Address(models.Model):
    address = models.CharField(max_length=500, null=True)
    code = models.CharField(max_length=5, null=True)
    city = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, default="France")
    def __unicode__(self):
        return self.address + self.code + self.city

class User(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    telephone = models.CharField(max_length=12, null=True, default="")
    email = models.EmailField(null=True, default="")
    address = models.ForeignKey(Address, null=True)
    def __unicode__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    address = models.ForeignKey(Address, null=True)
    def __unicode__(self):
        return self.name

class EventUser(models.Model):
    user = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    type = models.ForeignKey(UserType)
    def __unicode__(self):
        return self.user.name + ' - ' + self.event.name



class Plant(models.Model):
    name = models.CharField(max_length=64)
    local_name = models.CharField(max_length=64, null=True)
    scientific_name = models.CharField(max_length=64, null=True)
    variety_name = models.CharField(max_length=64, null=True)
    harvest_months = models.BinaryField(max_length=12, null=True)
    def __unicode__(self):
        return unicode(self.name)

class Area(models.Model):
    address = models.ForeignKey(Address)
    manager = models.ForeignKey(User)
    event = models.ForeignKey(Event)
    def __unicode__(self):
        return unicode(self.address)


class GleanablePlant(models.Model):
    plant = models.ForeignKey(Plant)
    size = models.CharField(max_length=64, null=True)
    vigour = models.CharField(max_length=64, null=True)
    properties = models.IntegerField(null=True)
    area = models.ForeignKey(Area)

class EventPlantGleaned(models.Model):
    event = models.ForeignKey(Event)
    gleanable_plant = models.ForeignKey(GleanablePlant)
    quantity = models.IntegerField(null=True)


###############################################################


class Project(models.Model):
    name = models.CharField(max_length=100)
    address = models.ForeignKey(Address, null=True)
    telephone = models.CharField(max_length=12, null=True)
    email = models.EmailField(null=True)
    web_site = models.URLField(default='http://')
    logo = models.ImageField(upload_to=user_directory_path)
    creation_date = models.PositiveIntegerField()
    reference = models.ForeignKey(User, null=True)
    owner_image = models.ImageField(null=True, upload_to=user_directory_path)
    structure_type = models.ForeignKey(StructureType, null=True)
    structure = models.CharField(max_length=100) ## A SUPPRIMER
    project_structure = models.ImageField(upload_to=user_directory_path)
    location_today = models.ImageField(upload_to=user_directory_path) ## A SUPPRIMER
    location_target = models.ImageField(upload_to=user_directory_path) ## A RELIER a une region/ville specifique
    workers = models.TextField() ## A NETTOYER
    def __unicode__(self):
        return unicode(self.name)



class Story(models.Model):
    description = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    content = models.TextField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    def __unicode__(self):
        return unicode(self.description)
