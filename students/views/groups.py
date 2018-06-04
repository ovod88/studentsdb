from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader



def groups_list(request):
	groups = (
		{'name': 'Мтм-21',
		'id': 1,
		'warden': {
			'name':'Віталій Подоба',
			'id': 1
			}
		},
		{'name': 'Мтм-22',
		'id': 2,
		'warden': {
			'name':'Андрій Петров',
			'id': 12
			}
		},
		{'name': 'Мтм-23',
		'id': 3,
		'warden': {
			'name': 'Андрій Подоба',
			'id': 14
			}
		}
	)
	# import pdb;pdb.set_trace()
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse(f'<h1>Edit Group {gid}</h1>')

def groups_delete(request, gid):
	return HttpResponse(f'<h1>Delete Group {gid}</h1>')