from django.shortcuts import  render, redirect
from .forms import UserForm, EditProfile, UpdatePassword
from .models import UserProfile
from django.urls import reverse, reverse_lazy
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordChangeView
import os
from django.conf import settings

def register_request(request):
	if request.method == "POST":
		form = UserForm(request.POST)
		if form.is_valid():
			form.save()
			user = form.save()
			login(request, user) 
			user_instance, created = UserProfile.objects.get_or_create(user=request.user)
			return redirect("index")
	else:
		form = UserForm() #show form
		
	return render(request, "account/register.html", {"create_user_form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request=request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				if request.POST.get('next')=="":
					return redirect("index")
				else:
					return redirect(request.POST.get('next')) 
	else:
		form = AuthenticationForm() 
	return render(request, "account/login.html", {"login_user_form":form})

def user_logout(request): 
	logout(request) 
	messages.success(request, 'Logged out!')
	return redirect(reverse('login'))

@login_required(login_url=reverse_lazy('login'))
def edit_profile(request):
	user_instance, created = UserProfile.objects.get_or_create(user=request.user)
	
	if request.method == "POST":
		#get_or_create returns a tuple of object , boolean (if creation successful)
		edit_profile_form = EditProfile(
			request.POST, 
			request.FILES, 
			instance=user_instance
		)
		if edit_profile_form.is_valid():
			avatar_to_delete = UserProfile.objects.get(user=request.user).avatar.url
			if(avatar_to_delete != "images/no_avatar.png"):
				os.remove(str(settings.BASE_DIR) + avatar_to_delete)
			edit_profile_form.save()
			messages.success(request, 'Your profile is edited')
			return redirect("index")
	else:
		edit_profile_form = EditProfile(instance=request.user)
		avatar = UserProfile.objects.get(user=request.user).avatar
		return render(
			request, 
			"account/edit.html", 
			{
				"edit_profile_form": edit_profile_form,
				"avatar": avatar
			}
		)

class PasswordUpdate(PasswordChangeView):
	form_class = UpdatePassword
	template_name = "account/change-password.html" #default required for PasswordChangeView
	success_url = reverse_lazy('update_password') #default required for PasswordChangeView
	#if form is valid, insert password success message by modifying form_valid method of base class
	def form_valid(self, form):
		messages.success(self.request, 'Your password has been changed.')
		return super().form_valid(form)
