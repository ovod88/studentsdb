from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from datetime import datetime
from calendar import monthrange


def journal_list(request):

	months = ['Styczen', 'Luty', 'Marzec', 'Kwieczen', 'Mai', 
				'Czerwiec', 'Lipiec', 'Sierpien', 'Wrzeszen', 'Padrziernik', 'Listopad', 'Grudzien']
	following_month = request.GET.get('month','')

	def countDateDict(date):
		newDate = {}
		newDate['month'] = months[date['month'] - 1]
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

	return render(request, 'students/journal.html', {'students': [{'name':'Віталій Подоба',
			'id': 1},{'name':'Андрій Петров',
			'id': 12},{'name': 'Андрій Подоба',
			'id': 14}], 'date': date, 'monthrange': range(days_in_month)})

def journal_student(request, sid):
	return HttpResponse(f'<h1>Journal for student {sid}</h1>')