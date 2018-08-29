from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, QueryDict
from django.template import RequestContext, loader

from datetime import datetime
from dateutil.relativedelta import relativedelta
from calendar import monthrange

import json

from ..models.students import Student
from ..models.groups import Group
from ..models.journals import Journal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.views.decorators.csrf import csrf_exempt

def journal_list(request, sid = None):

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
	elif sid:
		students = Student.students.filter(pk=sid)
	else:
		students = (Student.students.get_queryset().order_by('id'))

	def countDateDict(date):
		newDate = {}
		newDate['month_name'] = months[date['month'] - 1]

		cur_date = datetime(year=date['year'], month=date['month'], day=1)
		next_date = cur_date + relativedelta(months=1)
		prev_date = cur_date - relativedelta(months=1)
		# print(next_date)

		newDate['month'] = date['month']
		newDate['year'] = date['year']
		newDate['next_month'] = str(next_date.month) + '_' + str(next_date.year)
		newDate['prev_month'] = str(prev_date.month) + '_' + str(prev_date.year)

		# print('Created new date')
		# print(newDate)
		# print('----------------')

		return newDate 

	def addWhenStudentIsPresent(students):
		for student in students:

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

	if request.method == 'GET' and not sid:
		try:
			students = paginator.page(page)
		except PageNotAnInteger:
			students = paginator.page(1)
		except EmptyPage:
			students = paginator.page(paginator.num_pages)
		
		return render(request, 'students/journal.html', 
			{
				'students'   : students, 
				'date'       : date, 
				'monthrange' : range(1, days_in_month + 1), 
			})
	elif request.method == 'GET' and sid:
		# students = Student.students.filter(pk=sid)

		return render(request, 'students/journal.html', 
			{
				'students'   : students, 
				'date'       : date, 
				'monthrange' : range(1, days_in_month + 1), 
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
	if request.method == 'GET':#THIS IS A BAD SOLUTION. CHECK BOOK INSTEAD!!! IT IS WITH TEMPLATEVIEW
		return journal_list(request, sid)

	if request.method == 'POST':
		# print('DELETE HAS COME HERE')

		date_string = request.POST.get('date')
		date = datetime.strptime(date_string, '%d-%m-%Y')
		journal = Journal(student=Student.students.get(pk=sid), date=date)
		
		try:
			journal.save()
		except Exception as e:
			return JsonResponse({'status': 'nok'})

	if  request.method == 'DELETE':
		# print('DELETE HAS COME')

		delete_params = QueryDict(request.body)
		# import pdb;pdb.set_trace()

		date_string = delete_params.dict()['date']
		date = datetime.strptime(date_string, '%d-%m-%Y')
		journal = Journal.objects.filter(student=Student.students.get(pk=sid), date=date)
		
		try:
			journal.delete()
		except Exception as e:
			return JsonResponse({'status': 'nok'})

	return JsonResponse({'status': 'ok'})