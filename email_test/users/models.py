from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

class Profile(models.Model):
	user = models.OneToOneField(User)
	email_notifications = models.BooleanField(default=True)

class Subscriber(models.Model):
	email = models.EmailField()

from emails.notifications import welcome
def create_user_profile(sender, instance, created, **kwargs):
    if created:  
       profile, created = Profile.objects.get_or_create(user=instance)
       welcome(instance)

post_save.connect(create_user_profile, sender=User) 

