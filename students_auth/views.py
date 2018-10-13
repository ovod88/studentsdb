from django.shortcuts import render
from registration.backends.simple.views import RegistrationView as RegistrationBaseView
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class RegistrationView(RegistrationBaseView):
	def post(self, request, *args, **kwargs):
		if request.POST.get('register_cancel_button'):
			return HttpResponseRedirect(reverse('home'))
		else:
			return super().post(request, *args, **kwargs)
	