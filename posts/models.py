import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL

'''
models are tables in the database, you can import these model changes into the
database by running the commands python manage.py makemigrations and then
python manage.py migrate
'''

# table for 
class PostLike(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey("Post", on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

# table for a post, includes columns for defining user post data like the user, likes, content of post, etc
class Post(models.Model):
    """
    blank=True means that the value is not required in Django
    null=True means that the value is not required in the Database
    """
    # Maps to SQL Data
    # # id = models.AutoField(primary_key=True) 
    # this means if the comment on the post is deleleted, then the parent is set to NULL
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # many users can have many posts
    # through option is to allow for the timestamp functionality to work
    # it allows users to see when a post was created
    likes = models.ManyToManyField(User, related_name='post_user', blank=True, through=PostLike)
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    integer = models.SmallIntegerField(default=0, blank=True, null=True)

    # def __str__(self):
    #     return self.content

    class Meta:
        ordering = ['-id']

    @property
    def is_comment(self):
        return self.parent != None


    # Not needed anymore
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            'likes': random.randint(0, 200)
        }

class Test(models.Model):
    text = models.TextField(blank=True, null=True)
    time = models.DateTimeField(auto_now_add=True)
    integer = models.SmallIntegerField(default=0, blank=True, null=True)