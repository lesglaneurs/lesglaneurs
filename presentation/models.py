from django.db import models

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=100)
    logo = models.ImageField()
    photo = models.ImageField()
    creation_date = models.PositiveIntegerField()

    contact_name = models.CharField(max_length=100)
    email = models.EmailField()
    telephone = models.IntegerField()
    web_site = models.URLField()

    structure = models.CharField(max_length=100)
    func_image = models.ImageField()
    location = models.ImageField()

    def __unicode__(self):
        return unicode(self.name)


class Story(models.Model):
    description = models.CharField(max_length=200)
    project = models.ForeignKey(Project)
    content = models.TextField()
    logo = models.ImageField()
    coordinate_x = models.IntegerField()
    coordinate_y = models.IntegerField()
    def __unicode__(self):
        return unicode(self.description)

