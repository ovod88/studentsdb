from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader


def journal_list(request):
	return render(request, 'students/journal.html', {'students': [{'name':'Віталій Подоба',
			'id': 1},{'name':'Андрій Петров',
			'id': 12},{'name': 'Андрій Подоба',
			'id': 14}]})

def journal_student(request, sid):
	return HttpResponse(f'<h1>Journal for student {sid}</h1>')