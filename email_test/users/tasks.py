from __future__ import absolute_import
from celery.schedules import crontab
from celery.decorators import task, periodic_task


from django.contrib.auth.models import User

@task()
def send_activation_email(user_id):
	user = User.objects.get(pk=user_id)
	user.profile.send_welcome_email()

from users.models import *
from products.models import *
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

@periodic_task(run_every = crontab(minute=0, hour=0))
def email_digest():
	users = Profile.objects.filter(email_notifications = True)
	subscribers = Subscriber.objects.all()
	connection = mail.get_connection()
        connection.open()

	products = Product.objects.all()
	msg_plain = render_to_string('emails/products_digest.txt', {'product_list': products})
	msg_html = render_to_string('emails/products_digest.html', {'product_list': products})

	for each in users:
		subject, from_email, to = 'Daily Digest', 'products@productbyte.com', each.user.email
		msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to])
		msg.attach_alternative(msg_html, "text/html")
		msg.send()

	for each in subscribers:
		subject, from_email, to = 'Daily Digest', 'products@productbyte.com', each.email
		msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to])
		msg.attach_alternative(msg_html, "text/html")
		msg.send()
