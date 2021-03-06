from django.shortcuts import render
from django import forms
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from django.urls import reverse
from studentsdb.settings import ADMIN_EMAIL
from ..signals import email_admin_sent_signal

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django.contrib import messages
from django.contrib.messages import get_messages
import traceback

from django.contrib.auth.decorators import permission_required

import logging


def clear_messages(request):
	storage = get_messages(request)
	for message in storage:#removing all messages
		pass

@permission_required('auth.add_user')
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
				logger = logging.getLogger(__name__)
				logger.exception(message)
			else:
				email_admin_sent_signal.send(sender=None, from_=from_email, message=message)
				# redirect to same contact page with success message
				message = u'Повідомлення успішно надіслане!'
				messages.success(request, message)

		return HttpResponseRedirect(reverse('contact_admin'))
	# if there was not POST render blank form
	else:
		form = ContactForm()

		return render(request, 'contact_admin/form.html', {'form': form})

class ContactForm(forms.Form):

	def __init__(self, *args, **kwargs):
		# call original initializator
		super(ContactForm, self).__init__(*args, **kwargs)
		
		# this helper object allows us to customize form
		self.helper = FormHelper()
		
		# form tag attributes
		self.helper.form_class = 'form-horizontal'
		self.helper.form_method = 'post'
		self.helper.form_action = reverse('contact_admin')

		# twitter bootstrap styles
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		# form buttons
		self.helper.add_input(Submit('send_button', u'Надіслати'))
	
	from_email = forms.EmailField(
		label=u"Ваша Емейл Адреса")

	subject = forms.CharField(
		label=u"Заголовок листа",
		max_length=128)

	message = forms.CharField(
		label=u"Текст повідомлення",
		max_length=2560,
		widget=forms.Textarea)