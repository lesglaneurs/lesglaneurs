from django.db import models

# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/project_name/<filename>
    return '{0}/{1}'.format(instance.name, filename)

class Project(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ImageField(upload_to=user_directory_path)
    # creation_date = models.DecimalField(max_digits=8, decimal_places=0, default='9999')
    creation_date = models.PositiveIntegerField()
    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    # telephone = models.DecimalField(max_digits=10, decimal_places=0, default='0600000000')
    telephone = models.IntegerField()
    web_site = models.URLField(default='http://')

    structure = models.CharField(max_length=100)
    location_today = models.ImageField(upload_to=user_directory_path)
    location_target = models.ImageField(upload_to=user_directory_path)
    logo = models.ImageField(upload_to=user_directory_path)
    project_structure = models.ImageField(upload_to=user_directory_path)
    workers = models.TextField()

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

