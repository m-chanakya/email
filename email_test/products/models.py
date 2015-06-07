from django.db import models
from django.db.models.signals import post_save

class Product(models.Model):
	name = models.CharField(max_length = 50)

from emails.notifications import new_product_mail
from users.models import *
def send_notification(sender, instance, created, **kwargs):
    if created:
       users = Profile.objects.filter(email_notifications = True)
       subscribers = Subscriber.objects.all()
       for each in users:
         new_product_mail(each, instance)       
       for each in subscribers:
         new_product_mail(each, instance)       

post_save.connect(send_notification, sender=Product)
