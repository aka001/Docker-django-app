from django.shortcuts import render

# Create your views here.
import json
import os
from docker import Client
from django.core.mail import send_mail
from django.core import serializers
from django.utils.timezone import now as utcnow
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
import datetime
from datetime import datetime as dt
from django.core.urlresolvers import reverse
from django.template import RequestContext, loader
from finalapp.models import User, Containers
#from blood.models import Choice, Question, Donor, Recepient, Hospital, Camp, Link, Post, Story,Notification, User
from django.contrib.auth.decorators import login_required

cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
emailit="bloodconnect14@gmail.com"


@login_required
def index(request):
	context={}
	return render(request, 'finalapp/index.html',context)

@login_required
def home(request):
	context={}
	return render(request,'finalapp/home.html',context)

@login_required
def view_all_images(request):
	cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
	allimages=cli.images()
	print allimages
	context={}
	return render(request,'finalapp/view_all_images.html',context)

@login_required
def pull_images(request):
	context={}
	return render(request,'finalapp/pull_images.html',context)

@login_required
def create_container(request):
	context={}
	return render(request,'finalapp/create_container.html',context)
