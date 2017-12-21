# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, render_to_response, get_object_or_404
from django.template import Context, RequestContext

# Create your views here.
from django.http import HttpResponse

def index(request):
		return HttpResponse("""
<h1>idek</h1>
""")


def lookup(request):
	MAC_address = request.GET.get('MAC_address')
	
	context = {
		'MAC_address': MAC_address
	}

	return render_to_response('lookup.html', context, content_type=RequestContext(request))

