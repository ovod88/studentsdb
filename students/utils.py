from urllib.parse import unquote

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

def get_filter_values(request, cookie_name):
	try:
		# import pdb; pdb.set_trace()
		# print(request.COOKIES)

		cookie_value = request.COOKIES.get(cookie_name)
	except Exception as e:
		return ''
	else:
		if cookie_value is not None:
			return unquote(cookie_value)
		else:
			return ''
