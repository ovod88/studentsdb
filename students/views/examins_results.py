from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models.groups import Group
from ..models.examins_results import ExaminResult

def examins_results_list(request):

	groups_all = Group.objects.get_queryset().order_by('id')
	examins_results = ExaminResult.objects.get_queryset().order_by('id')

	return render(request, 'students/examins_results.html', {'examins_results': examins_results, 'groups_all': groups_all})

def examins_results_add(request):
	return HttpResponse('<h1>Examin Result Add Form</h1>')

def examins_results_edit(request, erid):
	return HttpResponse(f'<h1>Edit Examin Result {erid}</h1>')

def examins_results_delete(request, erid):
	return HttpResponse(f'<h1>Delete Examin Result {erid}</h1>')