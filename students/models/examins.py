from django.db import models

class Examin(models.Model):
	class Meta(object):
		verbose_name = u"Екзамін"
		verbose_name_plural = u"Екзаміни"

	title = models.CharField(
		max_length=256,
		blank=False,
		null=False,
		verbose_name=u"Назва")
	
	date = models.DateField(
		auto_now=False,
		auto_now_add=False,
		blank=False,
		null=False)

	examin_professor = models.ForeignKey("Professor",
		verbose_name=u"Викладач",
		blank=True,
		null=True,
		on_delete=models.CASCADE)

	examin_group = models.ForeignKey("Group",
		verbose_name=u"Група",
		blank=False,
		null=True,
		on_delete=models.CASCADE)
	
	def __str__(self):
		return "{}, {} by {} for {}".format(self.title, str(self.date), str(self.examin_professor),
											str(self.examin_group))

	def as_dict(self):
		return {
			"id" 	     : "%d" % self.id,
			"title"      : self.title if self.title else "",
			"date"       : str(self.date) if self.date else "",
			"professor"  : self.examin_professor if self.examin_professor else "",
			"group"      : self.examin_group if self.examin_group else ""
		}