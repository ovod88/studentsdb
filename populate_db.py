import sys

if __name__ == '__main__':
	import os
	import django
	import random_image_generator as image
	from studentsdb.settings import MEDIA_ROOT

	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studentsdb.settings')
	django.setup()

	import random

	from students.models.students import Student
	from students.models.journals import Journal
	from students.models.groups import Group
	from faker import Faker

	fakegen = Faker()
	groups = []
	leaders = []

	def populate(N=20):

		groups_titles = ['MTM-11', 'MTM-12', 'MTD-13', 'MTD-14']

		for i in range(4):
			groups.append(create_and_save_group(groups_titles[i]))

		for i in range(N):
			print("Entries for student {} are being added...".format(i))
			student = create_and_save_student()

			if len(leaders) < 4:
				leaders.append(student)

			for _ in range(N*2):
				create_and_save_journals(student)
				
			print("Entries for student {} are added...".format(i))

		
		for i in range(4):
			groups[i].leader = leaders[i]
			groups[i].save()



	def create_and_save_student():
		name = fakegen.name().split(' ')
		student_first_name = name[0]
		student_last_name = name[1]

		birthday = fakegen.date()

		photo = fakegen.file_name(category="image", extension="png")

		image.create_and_save_image(path=MEDIA_ROOT, filename=photo)

		ticket = random.randint(0, 1000)

		return Student.students.get_or_create(first_name=student_first_name, last_name=student_last_name,
										birthday=birthday, photo=photo, ticket=ticket,
										student_group=groups[random.randint(0, len(groups) - 1)])[0]

	def create_and_save_group(title):
		return Group.objects.get_or_create(title=title)[0]

	def create_and_save_journals(student):
		Journal.objects.get_or_create(student=student, date=fakegen.date_between(start_date="-60d", end_date="+60d"))

	print('-------- Start DB population ------------')

	import sys

	if len(sys.argv) > 1:
		populate(int(sys.argv[1]))
	else:
		populate()

	print('-------- End DB population -------------')