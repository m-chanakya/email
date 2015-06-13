# email
A test app to implement email notifications and a daily email digest

sudo apt-get install rabbitmq-server

pip install celery

celery -A email_test worker -B
