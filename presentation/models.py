from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)

class Project(models.Model):
    name = models.CharField(null=True,max_length=100, help_text="Le nom du projet")
    owner_image = models.ImageField(null=True,upload_to=user_directory_path)
    # creation_date = models.DecimalField(max_digits=8, decimal_places=0, default='9999')
    creation_date = models.PositiveIntegerField(null=True)
    contact_name = models.CharField(null=True,max_length=100)
    email = models.EmailField(null=True)
    # telephone = models.DecimalField(max_digits=10, decimal_places=0, default='0600000000')
    telephone = models.IntegerField(null=True)
    web_site = models.URLField(null=True)

    structure = models.CharField(null=True,max_length=100)
    location_today = models.ImageField(null=True,upload_to=user_directory_path)
    location_target = models.ImageField(null=True,upload_to=user_directory_path)
    logo = models.ImageField(null=True,upload_to=user_directory_path)
    project_structure = models.ImageField(null=True,upload_to=user_directory_path)
    workers = models.TextField(null=True)

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

class Event(models.Model):
    name = models.CharField(max_length=500)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    description = models.TextField(null=True, max_length=1000)
    project = models.ForeignKey(Project, null=True)
    def __unicode__(self):
        return self.name