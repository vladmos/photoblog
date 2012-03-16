from django.shortcuts import render_to_response
from django.template import RequestContext

def response(request, template, context=None):
    context = context or {}
    return render_to_response(template, context, context_instance=RequestContext(request))
