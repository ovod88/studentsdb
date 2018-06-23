from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from ..models import Student

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
	students=Student.objects.all()
	
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