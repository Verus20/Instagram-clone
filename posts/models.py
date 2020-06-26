from django.db import models

# Create your models here.
class Post(models.Model):
    """
    blank=True means that the value is not required in Django
    null=True means that the value is not required in the Database
    """ 
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)