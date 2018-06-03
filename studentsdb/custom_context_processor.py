def students_proc(request):

	return {'PORTAL_URL': request.build_absolute_uri('/')[:-1]}