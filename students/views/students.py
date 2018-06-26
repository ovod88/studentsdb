from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Student
from ..MyPaginator import MyPaginator

def students_list3(request):
	# students = (
	# 	{'id': 1,
	# 	'first_name': u'Віталій',
	# 	'last_name': u'Подоба',
	# 	'ticket': 235,
	# 	'image': 'img/podoba3.jpg'},
	# 	{'id': 2,
	# 	'first_name': u'Корост',
	# 	'last_name': u'Андрій',
	# 	'ticket': 2123,
	# 	'image': 'img/me.jpeg'},
	# 	{'id': 3,
	# 	'first_name': u'Притула',
	# 	'last_name': u'Тарас',
	# 	'ticket': 5332,
	# 	'image': 'img/piv.png'}
	# 	)
	# students = Student.objects.all()
	
	# students = Student.students.all()

	students = Student.students.get_queryset().order_by('id')

	order = request.GET.get('order_by','')
	page = request.GET.get('page')
	reverse = request.GET.get('reverse', '')

	# def ticket_sorting(student):
	# 	return int(student.ticket)

	if order in ('first_name', 'last_name'):
		students = students.order_by(order)

		if reverse == '1':
			students = students.reverse()

		# if order == 'ticket':
		# 	students = sorted(students, key=ticket_sorting, reverse=int(request.GET.get('reverse', '0')))
	
	#JUST FOR TESTING. DO NOT DO SORTINTG IN PYTHON ON PRODUCTION!!!USE CORRECT TYPE FIELDS
	if order == 'ticket':
		if reverse == '':
			students = Student.students.all_with_ticket_sorted(0)
		else:
			students = Student.students.all_with_ticket_sorted(int(request.GET.get('reverse', '0')))

	# print('-----HERE------')
	# print(students)

	if not request.GET or ((page is not None or page != '') and not order and not reverse):
		# print(type(students))
		students = students.order_by('last_name')

	paginator = MyPaginator(students, 3)
	# paginator = Paginator(students, 3)
	try:
		students = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		students = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver
		# last page of results.
		students = paginator.page(paginator.num_pages)




	groups = (
		{'name': 'Мтм-21',
		'warden': {
			'name':'Віталій Подоба',
			'id': 1
			}
		},
		{'name': 'Мтм-22',
		'warden': {
			'name':'Андрій Петров',
			'id': 12
			}
		},
		{'name': 'Мтм-23',
		'warden': {
			'name': 'Андрій Подоба',
			'id': 14
			}
		}
	)
	# import pdb;pdb.set_trace()
	return render(request, 'students/students_list.html', {'students': students, 'groups': groups})


def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse(f'<h1>Edit Student {sid}</h1>')

def students_delete(request, sid):
	return HttpResponse(f'<h1>Delete Student {sid}</h1>')