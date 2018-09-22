from django.db import models

class LogEntry(models.Model):

	class Meta(object):
		verbose_name=u"Log"
		verbose_name_plural = u"Logs"

	log_level = models.CharField(
		max_length=30,
		null=False,
		verbose_name=u"Log Level")

	date = models.DateTimeField(
		null=False,
		verbose_name=u"Date")

	module = models.CharField(
		max_length=100,
		null=False,
		verbose_name=u"Module")

	message = models.TextField(
		null=False,
		verbose_name=u"Message")

	def __str__(self):
		return "{} {} {}: {}".format(self.log_level, self.date, 
										self.module, self.id, self.message)

	def as_dict(self):
		return {
			"id"      : "%d" % self.id,
			"level"   : self.log_level,
			"date"    : self.date.strftime("%Y-%m-%d %H:%M:%S.%f"),
			"module"  : self.module,
			"message" : self.message
		}