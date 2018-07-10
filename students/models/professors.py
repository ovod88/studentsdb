from django.db import models

class Professor(models.Model):
	class Meta(object):
		verbose_name = u"Викладач"
		verbose_name_plural = u"Викладачі"

	first_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Ім'я")
	
	last_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Прізвище")

	email = models.EmailField(
		max_length=236,
		blank=False,
		verbose_name=u"Email",
		unique=True)
	
	def __str__(self):
		return "{}, {}".format(self.first_name, self.last_name,)

	def as_dict(self):
		return {
			"id" 	 : "%d" % self.id,
			"first_name"  : self.first_name if self.first_name else "",
			"last_name" : self.last_name if self.last_name else "",
			"email"  : self.email if self.email else ""
		}