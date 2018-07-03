from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Group

def groups_list(request):

	order = request.GET.get('order_by','')
	page = request.GET.get('page')
	reverse = request.GET.get('reverse', '')

	groups_all = Group.objects.get_queryset().order_by('id')
	# import pdb;pdb.set_trace()

	if order in ('title', 'leader'):
		if order == 'leader':
			groups = groups_all.order_by("leader__last_name")
		else:
			groups = groups_all.order_by(order)
		
		if reverse == '1':
			groups = groups_all.reverse()

	if not request.GET or (not order and not reverse):
		# print('CALLED DEFAULT ORDER')
		# print(type(students))
		groups = groups_all.order_by("title")

	paginator = Paginator(groups, 3)

	try:
		groups = paginator.page(page)
	except PageNotAnInteger:
		groups = paginator.page(1)
	except EmptyPage:
		groups = paginator.page(paginator.num_pages)


	return render(request, 'students/groups_list.html', {'groups': groups, 'groups_all': groups_all})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse(f'<h1>Edit Group {gid}</h1>')

def groups_delete(request, gid):
	return HttpResponse(f'<h1>Delete Group {gid}</h1>')