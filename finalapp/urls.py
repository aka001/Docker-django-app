from django.conf.urls import url 
from finalapp import views

urlpatterns = [ 
	url(r'^$', views.index, name='index'),
	url(r'^home/$',views.home,name='home'),
	url(r'^view_all_images/$',views.view_all_images,name='view_all_images'),
	url(r'^pull_images/$',views.pull_images,name='pull_images'),
	url(r'^create_container/$',views.create_container,name='create_container'),
	#url(r'^/$',views.view_request_thanks,name='view_request_thanks'),
]