from django.db import models
from django.contrib.auth.models import User
from django.core.mail import send_mail 
from django.template.loader import get_template 
from django.template import Context 
from django.conf import settings

# Create your models here.

class Category(models.Model):
	
	name = models.CharField(max_length=200)
	description = models.CharField(max_length=200)
	
	def __unicode__(self):
		return self.name

class Video(models.Model):
	
	url = models.CharField(max_length=255)
	name = models.CharField(max_length=200)
	category = models.ForeignKey(Category)
	description = models.CharField(max_length=200)
	likes = models.IntegerField()
	user = models.ForeignKey(User,null=True)
	views = models.IntegerField()
	created = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.name

	def get_absolute_url(self):
		return self.url

class Tag(models.Model):
	name = models.CharField(max_length=64, unique=True)
	videos = models.ManyToManyField(Video)

	def __unicode__(self):
		return self.name


class Friendship(models.Model):
	from_friend = models.ForeignKey(User, related_name='friend_set')
	to_friend = models.ForeignKey(User, related_name='to_friend_set')

	def __unicode__(self):
		values = {'from' : self.from_friend.username, 'to' : self.to_friend.username }
		return '[%(from)s] friend of [%(to)s]' % values


	class Meta: 
		unique_together = (('to_friend', 'from_friend'), )


class Invitation(models.Model):
	name = models.CharField(max_length=50)
	email = models.EmailField() 
	code = models.CharField(max_length=20)
	sender = models.ForeignKey(User) 

	def __unicode__(self):
		values = {'username' : self.sender.username, 'email' : self.email }
		return '[%(username)s], [%(email)s]' % values

	def send(self):
		subject = 'Invitation to join Spotifier'
		link = 'http://%s/friend/accept/%s/' % (settings.SITE_HOST, self.code )
		template = get_template('email/invitation_email.txt')
		context = Context({
			'name': self.name,
			'link': link,
			'sender': self.sender.username,
		})
		message = template.render(context)
		send_mail( subject, message, settings.DEFAULT_FROM_EMAIL, [self.email] )
