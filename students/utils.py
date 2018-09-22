def get_groups(request):
	from .models.groups import Group

	# groups_string = list(map(lambda group: str(group), Group.objects.all()))
	cur_group = get_current_group(request)

	groups = []

	for group in Group.objects.all().order_by('title'):
		groups.append({
			'id'       : group.id,
			'str'      : str(group),
			'selected' : cur_group and cur_group.id == group.id or False
		})

	return groups

def get_current_group(request):
	pk = request.COOKIES.get('current_group')

	if pk:
		from .models.groups import Group

		try:
			group = Group.objects.get(pk=int(pk))
		except Group.DoesNotExist:
			return None
		else:
			return group
	else:
		return None

def get_page_size(request):
	try:
		page_size = int(request.COOKIES.get('page_size'))
	except Exception as e:
		return None
	else:
		return page_size
