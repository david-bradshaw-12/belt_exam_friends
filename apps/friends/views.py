# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages
from models import *
import bcrypt

# Create your views here.
def login_page(request):
	return render(request, 'friends/login.html')

def friend_page(request, id):
	friend = Users.objects.get(id=id)
	their_friends = Users.objects.filter(friends=friend)
	context = {
		'friend': friend,
		'their_friends': their_friends
	}
	return render(request, 'friends/friend.html', context)

def main_friends(request):
	user_id = request.session['id']
	my_friends = Users.objects.filter(friends=Users.objects.get(id=user_id))
	User_nm = Users.objects.get(id=user_id)
	not_my_friends = Users.objects.exclude(friends=Users.objects.get(id=user_id))
	context = {
		'my_friends': my_friends,
		'user_name': User_nm,
		'not_my_friends': not_my_friends
	}
	return render(request, 'friends/main.html',context)

def add_friend(request):
	user_id = request.session['id']
	me = Users.objects.get(id=user_id)
	new_friend = Users.objects.get(id=(request.POST['friend_id']))
	me.friends.add(new_friend)
	return redirect('/main')

def remove_friend(request):
	user_id = request.session['id']
	me = Users.objects.get(id=user_id)
	old_friend = Users.objects.get(id=(request.POST['friend_id']))
	me.friends.remove(old_friend)
	return redirect('/main')

def register(request):
	if request.method == "POST":
		errors = Users.objects.basic_validation(request.POST)
		if len(errors):
			for tag, error in errors.iteritems():
				messages.error(request, error, extra_tags=tag)
				return redirect('/')
		email = request.POST['email']
		email_search = Users.objects.filter(email=email)
		if len(email_search) != 0:
			messages.error(request, "Email already exists")
			return redirect('/')
		name = request.POST['name']
		alias = request.POST['alias']
		dob = request.POST['dob']
		pw = request.POST['password']
		hash_pw = bcrypt.hashpw(pw.encode(), bcrypt.gensalt())
		pw2 = request.POST['password2']
		hash_pw2 = bcrypt.hashpw(pw2.encode(), bcrypt.gensalt())
		Users.objects.create(name=name, alias=alias, email=email, birthday=dob, password=hash_pw)
		#session login
		user1 = Users.objects.get(email=email)
		request.session['id'] = user1.id
		return redirect('/main')
	else:
		return redirect('/')

def login(request):
	log_email = request.POST['log_email']
	log_passw = request.POST['log_password']
	query = Users.objects.filter(email=log_email)
	if len(query) != 0:
		stord_pw = query[0].password
		if bcrypt.checkpw(log_passw.encode(), stord_pw.encode()) == False:
			messages.error(request, "Error:")
			messages.error(request, "It appears that is not your password")
			return redirect('/')
		else:
			#session log in
			request.session['id'] = query[0].id
			# print ('session id is ' + str(request.session['id']))#for testing purposes
			messages.error(request,"session log in")
			return redirect('/main')
	else:
		messages.error(request, "Error:")
		messages.error(request, "Cannot find your account.")
		return redirect('/')
	

def log_out(request):
	#session log out
	request.session.clear()
	return redirect('/')

# Create your views here.
