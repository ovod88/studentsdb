from registration.forms import *
from django.utils.translation import ugettext_lazy as _

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Field,Layout, Div, HTML
from crispy_forms.bootstrap import FormActions

from django.urls import reverse

class RegistrationForm(UserCreationForm):

	required_css_class = 'required'
	email = forms.EmailField(label=_("E-mail"))

	class Meta:
		model = User
		fields = (UsernameField(), "email")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		# import pdb;pdb.set_trace()

		self.helper = FormHelper(self)

		self.helper.form_action = reverse("registration_register")
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'

		self.helper.add_input(Submit('register_button', _(u'Register'), css_class="btn btn-primary"))
		self.helper.add_input(Submit('register_cancel_button', _(u'Cancel'), css_class="btn btn-link",
										formnovalidate='formnovalidate'))