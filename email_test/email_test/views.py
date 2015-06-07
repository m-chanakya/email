from django.shortcuts import render_to_response
from django.template.context import RequestContext

def home(request):
    context = RequestContext(request, {})
    return render_to_response('email_test/base.html', context_instance=context)
