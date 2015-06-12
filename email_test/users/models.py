from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Profile(models.Model):
	user = models.OneToOneField(User)
	email_notifications = models.BooleanField(default=True)

	def send_welcome_email(self):
		msg_plain = render_to_string('emails/welcome.txt', {'username': self.user.username})
		msg_html = render_to_string('emails/welcome.html', {'username': self.user.username})
		subject, from_email, to = 'Welcome', 'admin@productbyte.com', self.user.email
		msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to])
		msg.attach_alternative(msg_html, "text/html")
		msg.send()

class Subscriber(models.Model):
	email = models.EmailField()

def create_user_profile(sender, instance, created, **kwargs):
    if created:  
       profile, created = Profile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User) 

