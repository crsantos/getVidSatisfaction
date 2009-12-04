from django.conf.urls.defaults import *
from django.contrib import admin
from satisfaction.views import *
from django.views.generic.simple import direct_to_template
#from satisfaction.feeds import *
import os.path
site_media = os.path.join( os.path.dirname(__file__), 'site_media' )



admin.autodiscover()

urlpatterns = patterns('',
	# Example:
	# (r'^satisfaction_site/', include('satisfaction_site.foo.urls')),

	# ADMIN
	(r'^admin/', include(admin.site.urls)),

	#Browsing
	(r'^$', index), # null string = main-page
	(r'^video/(\d+)/$', video_page),
	(r'^user/(\w+)/$', user_page),
	
	#Saves
	(r'^save/$', save_video),
	
	#Recording
	(r'^rec/$', record),
	
	(r'^crossdomain.xml/$', direct_to_template, { 'template': 'satisfaction/crossdomain.xml' }),
	
	#Registration
	(r'^register/success/$', direct_to_template, { 'template': 'registration/register_success.html' }),

	#Site media
	(r'^site_media/(?P<path>.*)$', 'django.views.static.serve', { 'document_root': site_media }),
	
	# Comments 
	(r'^comments/', include('django.contrib.comments.urls')),
	
	
	# Feeds 
	#(r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed', {'feed_dict': feeds}),
	
	#Session management
	(r'^login/$', 'django.contrib.auth.views.login'),
	(r'^logout/$', logout_page),
	(r'^register/$', register_page),
	(r'^register/success/$', direct_to_template, { 'template': 'registration/register_success.html' }),

	# Friends 
	(r'^friends/(\w+)/$', friends_page),
	(r'^friend/add/$', friend_add),
	(r'^friend/invite/$', friend_invite),
	(r'^friend/accept/(\w+)/$', friend_accept),
)
