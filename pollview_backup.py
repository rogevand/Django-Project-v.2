# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse

def index(request):
	return HttpResponse("""
	<h1>This will be some meaningful shit eventually</h1>
	<h2>probably</h2>
	<h3>Work in progress by: Roger</h3>
	
	<form action="views.lookup">
		Please enter MAC address:
		<input type="text" name="MAC_address" value="">
		<input type="submit" value="Submit">
	</form>
	""")

def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
	response = "You're looking at the results of question %s."
	return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)