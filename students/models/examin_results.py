from django.db import models
from django.core.exceptions import ValidationError
from django import forms

class PositiveSmallIntegerFieldLimit(models.IntegerField):
    def __init__(self, verbose_name=None, name=None, min_value=None, max_value=None, **kwargs):
        self.min_value, self.max_value = min_value, max_value
        models.IntegerField.__init__(self, verbose_name, name, **kwargs)
        
    def formfield(self, **kwargs):
        defaults = {'min_value': self.min_value, 'max_value':self.max_value}
        defaults.update(kwargs)
        return super(PositiveSmallIntegerFieldLimit, self).formfield(**defaults)


class ExaminResult(models.Model):

	class Meta(object):
		verbose_name=u"Результат екзаміну"
		verbose_name_plural = u"Результати екзаміну"

	student = models.ForeignKey("Student",
		verbose_name=u"Студент",
		blank=False,
		null=False,
		on_delete=models.CASCADE)

	examin = models.ForeignKey("Examin",
		verbose_name=u"Екзамін",
		blank=False,
		null=False,
		on_delete=models.CASCADE)

	grade = PositiveSmallIntegerFieldLimit(
		min_value=1,
		max_value=6,
		blank=False,
		null=False)

	def __str__(self):
		return "{} passed {} with grade {}".format(self.student, self.examin.title, 
										self.grade)

	def __repr__(self):
		return "{} passed {} with grade {}".format(self.student, self.examin.title, 
										self.grade)