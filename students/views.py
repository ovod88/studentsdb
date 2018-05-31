from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


# Create your views here.
# def students_list(request):
# 	return HttpResponse('<h1>Hello World</h1>')


# def students_list2(request):
# 	template = loader.get_template('demo.html')
# 	context = RequestContext(request, {})

# 	return HttpResponse(template.render(context))


def students_list3(request):
	return render(request, 'students/students_list.html', {})


def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse(f'<h1>Edit Student {sid}</h1>')

def students_delete(request, sid):
	return HttpResponse(f'<h1>Delete Student {sid}</h1>')


def groups_list(request):
	return HttpResponse('<h1>Groups Listing</h1>')

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse(f'<h1>Edit Group {gid}</h1>')

def groups_delete(request, gid):
	return HttpResponse(f'<h1>Delete Group {gid}</h1>')