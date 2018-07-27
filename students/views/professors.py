from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group

def professors_list(request):

	return render(request, 'students/professors_list.html', {})

# def examins_add(request):
# 	return HttpResponse('<h1>Examin Add Form</h1>')

def professors_edit(request, pid):
	return HttpResponse(f'<h1>Edit Professor {pid}</h1>')

# def groups_delete(request, gid):
# 	return HttpResponse(f'<h1>Delete Group {gid}</h1>')