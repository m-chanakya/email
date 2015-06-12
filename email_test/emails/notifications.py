from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def new_product_mail(user, product):
	#Registered User
	if hasattr(user, 'user'):
		user = user.user
		username = user.username
	#Subscriber
	else:
		username = "Subscriber"

	msg_plain = render_to_string('emails/new_product.txt', {'username': username, 'product': product.name})
	msg_html = render_to_string('emails/new_product.html', {'username': username, 'product': product.name})

	subject, from_email, to = 'New Product', 'products@productbyte.com', user.email
	msg = EmailMultiAlternatives(subject, msg_plain, from_email, [to])
	msg.attach_alternative(msg_html, "text/html")
	msg.send()
