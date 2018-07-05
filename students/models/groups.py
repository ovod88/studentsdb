from django.db import models

class Group(models.Model):
	class Meta(object):
		verbose_name = u"Група"
		verbose_name_plural = u"Групи"

	title = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Назва")
	
	leader = models.OneToOneField("Student",# OneToOne relation between two tables
		verbose_name=u"Староста",
		blank=True,
		null=True,
		on_delete=models.SET_NULL)#If Student (leader) is deleted, this filed is set to NULL
									#but Student entry is allowed to be deleted

	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")
	
	def __str__(self):
		if self.leader:
			return "{} ({} {})".format(self.title, self.leader.first_name,self.leader.last_name)
		else:
			return "{}".format(self.title,)

	def as_dict(self):
		return {
			"id" 	 : "%d" % self.id,
			"title"  : self.title if self.title else "",
			"leader" : self.leader if self.leader else "",
			"notes"  : self.notes if self.notes else ""
		}