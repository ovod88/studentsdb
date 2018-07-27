from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group
from ..models.examins import Examin

def examins_list(request):

	examins = Examin.objects.get_queryset().order_by('id')

	return render(request, 'students/examins_list.html', {'examins': examins})

def examins_add(request):
	return HttpResponse('<h1>Examin Add Form</h1>')

def examins_edit(request, eid):
	return HttpResponse(f'<h1>Edit Examin {eid}</h1>')

def examins_delete(request, eid):
	return HttpResponse(f'<h1>Delete Group {eid}</h1>')