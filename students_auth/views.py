from django.shortcuts import render
from registration.backends.simple.views import RegistrationView as RegistrationBaseView
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from django.views.generic import View
# Create your views here.

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
	