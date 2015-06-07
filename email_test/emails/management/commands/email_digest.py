from django.core.management.base import BaseCommand, CommandError
from users.models import *
from products.models import *
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

class Command(BaseCommand):
    help = 'Sends periodic emails'

    def handle(self, *args, **options):
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

	self.stdout.write('Successfully emailed all Users')
	
	for each in subscribers:
		subject, from_email, to = 'Daily Digest', 'products@productbyte.com', each.email
        	msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to])
        	msg.attach_alternative(msg_html, "text/html")
        	msg.send()
	
	self.stdout.write('Successfully emailed all Subscribers')
	connection.close()
