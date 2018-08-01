from django.db import models

#ONLY TO TEST THE CASE THEN DB FIELD HAS WRONG DATATYPE
class TicketIntManager(models.Manager):
	def all_with_ticket_sorted(self, reverse):

		reverse_boolean = True

		if int(reverse) == 0:
			reverse_boolean = False

		students = self.get_queryset()

		def ticket_sorting(student):
			return int(student.ticket)

		list_students = sorted(students, key=ticket_sorting, reverse=reverse_boolean)
		list_ids = [student.id for student in list_students]

		clauses = ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(list_ids)])
		ordering = 'CASE %s END' % clauses

		"""
			SELECT *
			FROM students_student
			ORDER BY
  				CASE
    				WHEN id=4 THEN 0
    				WHEN id=5 THEN 1
    				WHEN id=6 THEN 2
    				WHEN id=8 THEN 3
    				WHEN id=7 THEN 4
    				.
    				.
  				END;
		"""
		queryset = students.filter(id__in=list_ids).extra(
           							select={'ordering': ordering}, order_by=('ordering',))


		return queryset
		
class Student(models.Model):

	class Meta(object):
		verbose_name=u"Студент"
		verbose_name_plural = u"Студенти"

	first_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Ім'я")

	last_name = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Прізвище")

	middle_name = models.CharField(
 		max_length=256,
 		blank=True,
		verbose_name=u"По-батькові",
		default='')

	birthday = models.DateField(
		blank=False,
		verbose_name=u"Дата народження",
		null=True)

	photo = models.ImageField(
 		blank=True,
		verbose_name=u"Фото",
 		null=True)

	ticket = models.CharField(
		max_length=256,
		blank=False,
		verbose_name=u"Білет")

	notes = models.TextField(
		blank=True,
		verbose_name=u"Додаткові нотатки")

	student_group = models.ForeignKey("Group",
		verbose_name=u"Група",
		blank=False,
		null=True,
		on_delete=models.PROTECT)#It wont allow group to be deleted while there is at least one student
								#pointing to it

	student_examin = models.ManyToManyField("Examin",
		verbose_name=u"Екзамін",
		blank=False,
		through="ExaminResult")

	def __str__(self):
		return "{},{},{},{} in group {}".format(self.first_name, self.last_name, 
										self.ticket, self.id, self.student_group)

	#JUST TO TEST TICKET SORTING BY CLASSMETHOD
	@classmethod
	def ticket_int(cls):
		return [int(s.ticket) for s in cls.students.all()]

	def get_ticket_int(self):
		return int(self.ticket)

	def as_dict(self):
		return {
			"id" 		 	: "%d" % self.id,
			"first_name" 	: self.first_name if self.first_name else "",
			"last_name"  	: self.last_name if self.last_name else "",
			"middle_name"	: self.middle_name if self.middle_name else "",
			"birthday"   	: self.birthday.strftime("%Y-%m-%d") if self.birthday else "",
			"photo"      	: str(self.photo) if self.photo else "",
			"ticket"     	: self.ticket if self.ticket else "",
			"notes"      	: self.notes if self.notes else "",
			"student_group" : self.student_group.title if self.student_group else ""
		}

	#JUST TO TEST CUSTOM DEFAULT MANAGER NAME
	# students=models.Manager()

	#JUST TASTE CUSTOM MANAGER WITH TICKET INT CONVERSION
	students = TicketIntManager()