from django.shortcuts import render

# Create your views here.
import httplib
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
from finalapp.models import User, Image, Container
#from blood.models import Choice, Question, Donor, Recepient, Hospital, Camp, Link, Post, Story,Notification, User
from django.contrib.auth.decorators import login_required

#cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
#emailit="bloodconnect14@gmail.com"


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
#	os.system('sudo su')
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/images/json")
        r1=conn.getresponse()
        r1=json.loads(r1.read())
        '''
        key=r1[0].keys()
        new_key=[]
        for i in key:
            new_key.append(str(i))'''
        context={'all_images':r1}
	return render(request,'finalapp/view_all_images.html',context)

#	cli = Client(base_url='unix://var/run/docker.sock',version='1.12')
#	allimages=cli.images()
#	print allimages
#	context={}
#	return render(request,'finalapp/view_all_images.html',context)



@login_required
def ask_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        name= request.POST['name']
        return HttpResponseRedirect('/finalapp/pull_images/'+(name)+'/')
    context={'user':user}
    return render(request,'finalapp/ask_images.html',context)


@login_required
def pull_images(request,name):
    conn=httplib.HTTPConnection("localhost:4243")
    image_pull='/images/create?fromImage='
    image_pull+=str(name)
    print image_pull
    conn.request("POST",image_pull)
    r1=conn.getresponse()
    a=r1.read()
    r1=a
    #key=r1[0].keys()
    #new_key=[]
    flag=0
    if 'error' not in r1:
        flag=0
        r1=r1.split('\n')[0]
        print r1
        #if "" in r1:
        print "hie hie"
        form = Image()
        form.uid=request.user.id
        #parse_json=json.loads(check)
        r1=json.loads(r1)
        form.id_images=r1['id']
        form.save()
        '''else:
            flag=1'''
    else:
        flag=2
    context={'name':name, 'flag':flag}
    return render(request,'finalapp/pull_images.html',context)


@login_required
def ask_create_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        image= request.POST['image']
        return HttpResponseRedirect('/finalapp/create_container/'+(image)+'/')

    uuid=request.user.id
    image_list=Image.objects.all().filter(uid=uuid)
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_create_container.html',context)

    
@login_required
def create_container(request,image):
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print image
    new_req_body = '{"Hostname":"","User":"","Memory":0,"MemorySwap":0,"AttachStdin":false,"AttachStdout":true,"AttachStderr":true,"ExposedPorts":{},"Tty":false,"OpenStdin":false,"StdinOnce":false,"Env":null,"Cmd":["date"],"Dns":null,"Image":"'
    new_req_body += str(image)
    new_req_body += '","Volumes":{},"VolumesFrom":"","WorkingDir":""}'
    new_conn.request("POST", "/containers/create", new_req_body, headers)
    r1 = new_conn.getresponse().read()
    r1=json.loads(r1)
    form=Container()
    form.uid=request.user.id
    form.name_image=image
    form.id_container=r1['Id']
    form.save()
    print r1['Id']   
    #print r1.status
    #conn=httplib.HTTPConnection("localhost:4243")    
    #conn.request("POST", "/containers/create",request_body)
    #r1=conn.getresponse()
    #create_container='/images/create?fromImage='
    #print r1.status
    context={'name':r1}
    return render(request,'finalapp/create_container.html',context)

@login_required
def view_all_containers(request):
#	os.system('sudo su')
        conn=httplib.HTTPConnection("localhost:4243")
        conn.request("GET","/containers/json")
        r1=conn.getresponse()
        print r1.status
        a=r1.read()
        print a
        context={'all_containers':a}
	return render(request,'finalapp/view_all_containers.html',context)


@login_required
def ask_search_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        name = request.POST['search_name']
        print "asdasd"
        return HttpResponseRedirect('/finalapp/search_images/'+(name)+'/')
    context={'user':user}
    return render(request,'finalapp/ask_search_images.html',context)

@login_required
def search_images(request,search_name):
    conn=httplib.HTTPConnection("localhost:4243")
    image_search='/images/search?term='
    image_search+=str(search_name)
    conn.request("GET",image_search)
    r1=conn.getresponse()
    print r1.status
    value=r1.read()
    print search_name,value
    context={'search_name':search_name, 'value':value}
    return  render(request, 'finalapp/search_images.html',context)

@login_required
def ask_del_images(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        idd= request.POST['id']
        print "asdasd"
        return HttpResponseRedirect('/finalapp/delete_images/'+(idd)+'/')
    uuid=request.user.id
    image_list=Image.objects.all().filter(uid=uuid)
    image_id=[]
    for images in image_list:
        image_id.append(images.id_images)
    context={'user':user, 'image_id':image_id}
    return render(request,'finalapp/ask_del_images.html',context)

@login_required
def delete_images(request,idd):
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/images/'
    image_del+=str(idd)
    print image_del
    conn.request("DELETE",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=r2.read()
    print r2
    if "error" not in r2:
        print idd
        Image.objects.filter(id_images=idd).delete()
    #print r1.read()
    #r1=r1.read()
    context={'idd':idd}
    return render(request, 'finalapp/delete_images.html', context)

@login_required
def ask_stop_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/stop_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_stop_container.html',context)
 
 
 
@login_required
def stop_container(request,container_id):
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_req_body='{"Binds":["/tmp:/tmp"], "Links":["redis3:redis"], "LxcConf":{"lxc.utsname":"docker"},"PortBindings":{ "22/tcp": [{ "HostPort": "11022" }] },"PublishAllPorts":false, "Privileged":false, "Dns": ["8.8.8.8"],"DnsSearch": [""],"VolumesFrom": ["parent", "other:ro"], "CapAdd": ["NET_ADMIN"], "CapDrop": ["MKNOD"],"RestartPolicy": { "Name": "", "MaximumRetryCount": 0 },"NetworkMode": "bridge","Devices": []}'
    new_conn.request("POST", "/containers/" + container_id + "/stop" , new_req_body, headers)
    r1 = new_conn.getresponse().read()
    print r1
    context={'name':r1,'name':container_id}
    return render(request,'finalapp/stop_container.html',context)

@login_required
def ask_start_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/start_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_start_container.html',context)
 
 
@login_required
def start_container(request,container_id):
    container_id=container_id[0:3]
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_req_body='{"Binds":["/tmp:/tmp"], "Links":["redis3:redis"], "LxcConf":{"lxc.utsname":"docker"},"PortBindings":{ "22/tcp": [{ "HostPort": "11022" }] },"PublishAllPorts":false, "Privileged":false, "Dns": ["8.8.8.8"],"DnsSearch": [""],"VolumesFrom": ["parent", "other:ro"], "CapAdd": ["NET_ADMIN"], "CapDrop": ["MKNOD"],"RestartPolicy": { "Name": "", "MaximumRetryCount": 0 },"NetworkMode": "bridge","Devices": []}'
    new_conn.request("POST", "/containers/" + container_id + "/start" , new_req_body, headers)
    r1 = new_conn.getresponse().read()
    context={'name':r1,'name':container_id}
    return render(request,'finalapp/start_container.html',context)

@login_required
def ask_del_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/delete_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_del_container.html',context)
 
@login_required
def delete_container(request,container_id):
    container_id=container_id[0:3]
    conn=httplib.HTTPConnection("localhost:4243")
    container_del='/containers/'
    container_del+=str(container_id)
    print container_del
    conn.request("DELETE",container_del)
    r2=conn.getresponse()
    print r2.status
    #print r1.read()
    #r1=r1.read()
    context={'container_id':container_id}
    return render(request, 'finalapp/delete_container.html', context)

@login_required
def ask_restart_container(request):
    if request.user.is_authenticated:
        user=request.user.username
    if request.method == 'POST':
        container_id = request.POST['container_id']
        return HttpResponseRedirect('/finalapp/restart_container/'+(container_id)+'/')
    conn=httplib.HTTPConnection("localhost:4243")
    image_del='/containers/json?all=1'
    print image_del
    conn.request("GET",image_del)
    r2=conn.getresponse()
    print r2.status
    r2=json.loads(r2.read())
    image_id=[]
    for image in r2:
        image_id.append(image['Id'])
    context={'user':user,'image_id':image_id}
    return render(request,'finalapp/ask_restart_container.html',context)
 
@login_required
def restart_container(request,container_id):
    container_id=container_id[0:4]
    new_conn = httplib.HTTPConnection('172.17.42.1:4243')
    headers = {"Content-type": "application/json","Accept": "text/plain"}
    print container_id
    new_conn.request("POST", "/containers/" + container_id + "/restart" , headers)
    r1 = new_conn.getresponse().read()
    print r1
    context={'name':r1}
    return render(request,'finalapp/restart_container.html',context)

