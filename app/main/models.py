from django.db import models

class VostrebContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class SkillsContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()

class GeorgraphContent(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
class Image(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to='images')

    def __str__(self):
        return self.title