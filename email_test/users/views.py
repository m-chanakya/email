from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from .forms import UserForm, SubscriberForm

from users.tasks import send_activation_email

@csrf_exempt
def create(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
		username, email, password = form.cleaned_data['username'], form.cleaned_data['email'], form.cleaned_data['password1']
		new_user = User.objects.create_user(username, email, password)
		new_user.save()
		send_activation_email(user_id = new_user.pk)
            	return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()
    return render(request, 'users/signup.html', {'form': form})

@csrf_exempt
def subscribe(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SubscriberForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            form.save()
            return HttpResponseRedirect('/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = SubscriberForm()

    return render(request, 'users/subscribe.html', {'form': form})
