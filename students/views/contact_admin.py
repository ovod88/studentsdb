from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from studentsdb.settings import ADMIN_EMAIL

from django.contrib import messages
from django.contrib.messages import get_messages
import traceback

def clear_messages(request):
	storage = get_messages(request)
	for message in storage:#removing all messages
		pass


def contact_admin(request):
	# check if form was posted
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = ContactForm(request.POST)

		# check whether user data is valid:
		if form.is_valid():
			# send email
			subject = form.cleaned_data['subject']
			message = form.cleaned_data['message']
			from_email = form.cleaned_data['from_email']

			clear_messages(request)
			
			try:
				send_mail(subject, message, from_email, [ADMIN_EMAIL])
			except Exception as e:
				message = u'Під час відправки листа виникла непередбачувана помилка. \
							Спробуйте скористатись даною формою пізніше.'
				messages.error(request, message)
				traceback.print_exc()
			else:
				# redirect to same contact page with success message
				message = u'Повідомлення успішно надіслане!'
				messages.success(request, message)

		return HttpResponseRedirect(reverse('contact_admin'))
	# if there was not POST render blank form
	else:
		form = ContactForm()

		return render(request, 'contact_admin/form.html', {'form': form})

class ContactForm(forms.Form):
	from_email = forms.EmailField(
		label=u"Ваша Емейл Адреса")

	subject = forms.CharField(
		label=u"Заголовок листа",
		max_length=128)

	message = forms.CharField(
		label=u"Текст повідомлення",
		max_length=2560,
		widget=forms.Textarea)