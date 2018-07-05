from django.db import models

class Journal(models.Model):

	class Meta(object):
		verbose_name=u"Журнал відвідування"
		verbose_name_plural = u"Журнали відвідування"
		unique_together=(('student', 'date'))

	student = models.ForeignKey("Student",
		verbose_name=u"Студент",
		blank=False,
		null=False,
		on_delete=models.CASCADE)

	date = models.DateField(
		auto_now=False,
		auto_now_add=False,
		blank=False,
		null=False)

	def __str__(self):
		return "{} - {},{} from {}".format(self.date, self.student.first_name, 
										self.student.last_name, 
										self.student.student_group.title)