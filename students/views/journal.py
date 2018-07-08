from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import RequestContext, loader

from datetime import datetime
from calendar import monthrange

from ..models.students import Student
from ..models.groups import Group
from ..models.journals import Journal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def journal_list(request):

	months = ['Styczen', 'Luty', 'Marzec', 'Kwieczen', 'Mai', 
				'Czerwiec', 'Lipiec', 'Sierpien', 'Wrzeszen', 'Padrziernik', 'Listopad', 'Grudzien']

	following_month = request.GET.get('month','')
	order = request.GET.get('order_by','')
	page = request.GET.get('page')
	reverse = request.GET.get('reverse', '')

	if order in ('last_name',):
		students = (Student.students.get_queryset().order_by('last_name'))

		if reverse == '1':
			students = students.reverse()
	else:
		students = (Student.students.get_queryset().order_by('id'))

	def countDateDict(date):
		newDate = {}
		newDate['month_name'] = months[date['month'] - 1]
		newDate['month'] = date['month']
		newDate['year'] = date['year']

		if date['month'] == 12:
			newDate['next_month'] = str(1) + '_' + str(date['year'] + 1)
			newDate['prev_month'] = str(date['month'] - 1) + '_' + str(date['year'])
		elif date['month'] == 1:
			newDate['next_month'] = str(date['month'] + 1) + '_' + str(date['year'])
			newDate['prev_month'] = str(12) + '_' + str(date['year'] - 1)
		else:
			newDate['next_month'] = str(date['month'] + 1) + '_' + str(date['year'])
			newDate['prev_month'] = str(date['month'] - 1) + '_' + str(date['year'])

		# print('Created new date')
		# print(newDate)
		# print('----------------')

		return newDate 

	def addWhenStudentIsPresent(students):
		for student in students:
			# days = (Journal.objects.all().filter(student=student, 
			# 									   date__year=cur_year, date__month=cur_month)
			# 								.dates('date', 'day'))
			# present_days = list(map(lambda date: date.day, days))
			# student.days(present_days)
			days = student.journal_set.filter(date__year=cur_year, date__month=cur_month).dates('date','day')
			student.days = list(map(lambda date: date.day, days))


	if following_month:
		(cur_month, cur_year) = following_month.split('_')
		cur_month = int(cur_month)
		cur_year = int(cur_year)

		date = countDateDict({
			'month' : cur_month,
			'year' : cur_year
			})

	else:
		today = datetime.today()
		cur_month = today.month
		cur_year = today.year
		date = countDateDict({
				'month': cur_month,
				'year' : cur_year
			})

	days_in_month = monthrange(cur_year, cur_month)[1]

	# print(days_in_month)

	addWhenStudentIsPresent(students)

	# for student in students:
	# 	print(student.days)

	paginator = Paginator(students, 3)

	if request.method == 'GET':
		try:
			students = paginator.page(page)
		except PageNotAnInteger:
			students = paginator.page(1)
		except EmptyPage:
			students = paginator.page(paginator.num_pages)

		groups_string = list(map(lambda group: str(group), Group.objects.all()))
		
		return render(request, 'students/journal.html', 
			{
				'students'   : students, 
				'date'       : date, 
				'monthrange' : range(1, days_in_month + 1), 
				'groups_all' : groups_string
			})


	if request.method == 'POST':
		load_more = request.POST.get('load_more', False)
		ajax_page = request.POST.get('ajax_page')
		if ajax_page and load_more:

			ajax_page = int(ajax_page)
			if ajax_page <= paginator.num_pages:
				students = paginator.page(ajax_page)
			else:
				students = []
		else:
			students = []

		students_page = list(map(lambda student: {
								"id" 			: "%d" % student.id,
								"first_name" 	: student.first_name if student.first_name else "",
								"last_name"  	: student.last_name if student.last_name else "",
								"days"          : student.days if student.days else []
							}, students))

		return JsonResponse({'students': students_page, 'date': date})

	# return render(request, 'students/journal.html', {'students': [{'name':'Віталій Подоба',
	# 		'id': 1},{'name':'Андрій Петров',
	# 		'id': 12},{'name': 'Андрій Подоба',
	# 		'id': 14}], 'date': date, 'monthrange': range(days_in_month)})

def journal_student(request, sid):
	if request.method == 'POST':
		print('POST came' + sid)

		return JsonResponse({'status': 'ok'})