from django.shortcuts import render
from registration.backends.simple.views import RegistrationView as RegistrationBaseView
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import View, UpdateView
from .models import StProfile
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import get_messages
from .forms import UserEditMultiForm

# Create your views here.

def clear_messages(request):
	# list(messages.get_messages(request))#DOES THE SAME
	storage = get_messages(request)
	for message in storage:#removing all messages
		pass

class AbstractLoginRequiredView():

	@method_decorator(login_required)
	def dispatch(self, *args, **kwargs):
		return View.dispatch(self, *args, **kwargs)

class RegistrationView(RegistrationBaseView):
	def post(self, request, *args, **kwargs):
		if request.POST.get('register_cancel_button'):
			return HttpResponseRedirect(reverse('home'))
		else:
			return super().post(request, *args, **kwargs)

class ProfileUpdateView(AbstractLoginRequiredView, UpdateView):
	# model = User
	form_class = UserEditMultiForm
	template_name='registration/profile_edit.html'
	# form_class = StudentUpdateForm

	def get_success_url(self):

		clear_messages(self.request)

		messages.success(self.request, 'Профіль оновлено!')

		return reverse('profile')

	def form_invalid(self, form):
		message = 'Form was filled incorrectly by user {}'.format(form.instance.id)
		
		# logger = logging.getLogger('database')

		print(message)
		# logger.warning(message)
		
		# send_mail('Edit form notification', message, ADMIN_EMAIL, [ADMIN_EMAIL])


		return super().form_invalid(form)

	def post(self, request, *args, **kwargs):
		# print(kwargs)
		if request.POST.get('cancel_button'):
			clear_messages(request)

			messages.info(request, 'Редагування профілю відмінено!')

			return HttpResponseRedirect(reverse('profile'))
		else:
			return super().post(request, *args, **kwargs)
	
	# def get_context_data(self, **kwargs):
	# 	kwargs = super().get_context_data(**kwargs)
	# 	print(kwargs)
	# 	return kwargs
	def get_object(self, queryset=None):
		# print(self.request.user.stprofile.mobile_phone)
		obj = StProfile.objects.get(user=self.request.user)
		# print(obj.user.password)
		return obj


	def get_form_kwargs(self):
		kwargs = super().get_form_kwargs()
		kwargs.update(instance={
			'user': self.object.user,
			'profile': self.object
		})
		return kwargs
