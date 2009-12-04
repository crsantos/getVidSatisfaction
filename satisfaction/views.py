from django.shortcuts import render_to_response, get_object_or_404
from django.core.exceptions import ObjectDoesNotExist
from satisfaction.models import *
from satisfaction.forms import *
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.contrib.auth.models import User 
from django.template import Context
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.template import RequestContext
from datetime import datetime, timedelta, date
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q
import re
from django import forms
from django.utils.translation import ugettext as _
from random import randint
from cStringIO import StringIO
from reportlab.pdfgen import canvas
from django.core.cache import cache
from django.utils.translation import check_for_language
from django.contrib.sitemaps import ping_google
#import twitter

ugettext = lambda s:s

ITEMS_PER_PAGE=5
LAST_X_DAYS=10

SERVER_IP='213.13.77.93'

title= "Satisfaction"
heading=_('Satisfaction')

def index(request):
	
	# videos = Video.objects.order_by( '-created' )#[:10]
	# try: #tries to get the page by GET
	# 	page = int(request.GET['page'])
	# except: 
	# 	page = 1
	# 
	# paginator = Paginator(videos, ITEMS_PER_PAGE)
	# p = paginator.page(page)
	# videos = p.object_list
	# 
	# return render_to_response('satisfaction/index.html',
	# 	{
	# 		'title': title,
	# 		'heading': heading,
	# 		'user': request.user,
	# 		'cenas': request.session.get("django_language", None),
	# 		'videos': videos
	# 	})
	
	return render_to_response('satisfaction/start_rec.html',
	{
		'title': title,
		'heading': heading,
		'user': request.user
	})

def request(request):
	return HttpResponse('')

def record(request):

	# if request.method == 'POST':
	# 	form = VideoSaveForm( request.POST )
	# 	
	# 	video, created = Video.objects.get_or_create(
	# 			#url=form.cleaned_data['url'],
	# 			categoria=form.cleaned_data['categoria']
	# 	)
	# 	if not created:
	# 		video.tag_set.clear()
	# 	tag_names = form.cleaned_data['tags'].split(', ')
	# 	for tag_name in tag_names:
	# 		if len(tag_name)>1:
	# 			tag_name.strip()
	# 			tag, dummy = Tag.objects.get_or_create(name=tag_name)
	# 			video.tag_set.add(tag)
	# else:
	# 	form = VideoSaveForm()
		
	return render_to_response('satisfaction/rec.html',
	{
		'title': title,
		'user': request.user,
		'server': SERVER_IP
		# 'form': form
	})


def save_video(request):
	
	if request.method == 'GET' and 'url' in request.GET:# and request.META.get('REMOTE_ADDR')==SERVER_IP:
		url= "http://"+SERVER_IP+":6666/videos/"+request.GET.get('url')+".flv"
		if len(url)>0:
			video = Video.objects.create(
									url=url,
									category=Category.objects.get(id=1),
									likes=0,
									views=0,
									name=request.GET.get('url'),
									user=User.objects.get(id=1)
				)
			
			#return HttpResponse("%s" % video.id)
			print "RECEBI DO: %s" % request.META.get('REMOTE_ADDR')
			return HttpResponseRedirect('/video/%d' %video.id)
			
	else:
		return HttpResponse("ESTUDASSES, goza cu c*r*lho!")
		
	
	
		

def logout_page(request):
	logout(request)
	return HttpResponseRedirect('/')
	
def register_page(request):

	if request.method == 'POST':
		form = RegistrationForm( request.POST )

		if form.is_valid():
			user = User.objects.create_user(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password1'],
				email=form.cleaned_data['email']
			)

			profile = UserProfile.objects.get_or_create(
				user=user,
				institution=form.cleaned_data['institution'],
				gender=form.cleaned_data['gender'],
				address=form.cleaned_data['address'],
				housing=form.cleaned_data['housing'],
				observations=form.cleaned_data['observations'],
				phone=form.cleaned_data['phone']
			) 

			if 'invitation' in request.session:
				# Retrieve the invitation object.
				invitation = \
				Invitation.objects.get(id=request.session['invitation'])
				# Create friendship from user to sender.
				friendship = Friendship(
					from_friend=user,
					to_friend=invitation.sender
				)
				friendship.save()
				# Create friendship from sender to user.
				friendship = Friendship (
					from_friend=invitation.sender,
					to_friend=user
				)
				friendship.save()
				# Delete the invitation from the database and session.
				invitation.delete()
				del request.session['invitation']

			return HttpResponseRedirect('/register/success/')

	else:
		form = RegistrationForm()

	return render_to_response(
		'registration/register.html', {
		'form': form
		}
	)	

def video_page(request,id):
	
	#Get the video
	video = get_object_or_404( Video,id=id)
	
	videos = Video.objects.order_by( '-created' ).exclude(id=id)
	
	return render_to_response('satisfaction/video_page.html',
		{
			'video': video,
			'videos': videos,
			'title': title,
			'user': request.user
		})
	

@login_required
def user_page(request,username):

	heading= "Videos for "+username
	try:
		user = User.objects.get(username=username)
	except:
		raise Http404('Requested user not found.')

	videos = user.video_set.all()

	# if request.user:
	# 	is_friend = Friendship.objects.filter(
	# 		from_friend=request.user,
	# 		to_friend=user
	# 	)

	try: #tries to get the page by GET
		page = int(request.GET['page']) 
	except: 
		page = 1

	paginator = Paginator(videos, ITEMS_PER_PAGE)
	p = paginator.page(page)
	videos = p.object_list

	return render_to_response('satisfaction/user_page.html',
		{
			'username': username,
			'videos': videos,
			'title': title,
			'heading': heading,
			'user': request.user,
			'show_tags': True,
			'show_edit': username == request.user.username,
			'show_paginator': paginator.num_pages > 1,
			'has_prev': p.has_previous(),
			'has_next': p.has_next(),
			'page': int(page),
			'pages': paginator.page_range,
			'prev': p.previous_page_number(),
			'next': p.next_page_number()
			#'is_friend': is_friend
		})

def friends_page(request, username):
	user = get_object_or_404(User, username=username) 
	friends = \
		[friendship.to_friend for friendship in user.friend_set.all()] 
	friend_videos = \
		Video.objects.filter(user__in=friends).order_by('-id') 
	variables = RequestContext(request, {
		'username': username, 
		'friends': friends, 
		'videos': friend_videos[:10], 
		'show_tags': True, 
		'show_user': True 
	})
	return render_to_response('satisfaction/friends_page.html', variables)


@login_required
def friend_add(request): 
	if request.GET.has_key('username'): 
		friend = \
		get_object_or_404(User, username=request.GET['username']) 
		friendship = Friendship( 
		from_friend=request.user, 
		to_friend=friend 
		)

		try:
			friendship.save()
			request.user.message_set.create( message='%s was added to your friend list.' % friend.username )
		except:
			request.user.message_set.create( message='%s is already a friend of yours.' % friend.username )

		return HttpResponseRedirect('/friends/%s/' % request.user.username
		)
	else: 
		raise Http404


@login_required
def friend_invite(request): 
	if request.method == 'POST': 
		form = FriendInviteForm(request.POST) 
		if form.is_valid(): 
			invitation = Invitation( 
				name = form.cleaned_data['name'], 
				email = form.cleaned_data['email'], 
				code = User.objects.make_random_password(20), 
				sender = request.user 
			)

			invitation.save() # saves invitation

			try:
				invitation.send() #tries to send() invitation
				request.user.message_set.create( message='An invitation was sent to %s.' % invitation.email )
			except:
				request.user.message_set.create( message='There was an error while sending the invitation.' )

			return HttpResponseRedirect('/friend/invite/') 
	else: 
		form = FriendInviteForm()
	variables = RequestContext(request, {
			'form': form
	})
	return render_to_response('spotifier/friend_invite.html', variables)


def friend_accept(request, code):
	invitation = get_object_or_404(Invitation, code__exact=code)
	request.session['invitation'] = invitation.id
	return HttpResponseRedirect('/register/')
	
