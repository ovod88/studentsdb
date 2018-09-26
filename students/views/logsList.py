from django.views.generic import ListView
from students.models.logentry import LogEntry
from ..utils import get_filter_values

class LogsList(ListView):

	model = LogEntry
	context_object_name = 'logs'
	template_name = 'students/logs.html'
	queryset = LogEntry.objects.all().order_by('date').reverse()
	paginate_by = 10

	def get_context_data(self, **kwargs):

		page_size = super().get_paginate_by(self.queryset)
		context_object_name = self.get_context_object_name(self.queryset)

		if page_size:
			paginator, logs_page, logs, if_paginated = super().paginate_queryset(self.queryset, page_size)
			context = {
				'logs_page' : logs_page,
				'page_size' : page_size
			}
		else:
			context = {
				'logs_page' : None,
				'page_size' : page_size
			}

		context.update(kwargs)

		if context_object_name is not None:
			context[context_object_name] = logs
		return context

	def get(self, request, *args, **kwargs):
		try:
			page_size = int(get_filter_values(request, 'page_size'))
		except Exception as e:
			# print(e)
			page_size = None

		log_level = get_filter_values(request, 'log_level')
		date = get_filter_values(request, 'date')
		module = get_filter_values(request, 'module')
		message = get_filter_values(request, 'message')

		# print(page_size)
		# print(log_level)
		# print(date)
		# print(module)
		# print(message)

		self.queryset = LogEntry.objects.filter(log_level__contains=log_level,
												date__contains=date,
												module__contains=module,
												message__contains=message)

		print(self.queryset);

		if page_size is not None:
			self.paginate_by = page_size

		return super().get(request, *args, **kwargs)

