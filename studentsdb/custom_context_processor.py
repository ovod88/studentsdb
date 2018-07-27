from students.models.groups import Group

def students_proc(request):

	groups_string = list(map(lambda group: str(group), Group.objects.all()))
	
	return {'PORTAL_URL': request.build_absolute_uri('/')[:-1],
				'groups_all' : groups_string}