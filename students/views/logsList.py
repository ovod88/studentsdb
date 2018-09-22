from django.views.generic import ListView
from students.models.logentry import LogEntry
from ..utils import get_page_size

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
		page_size = get_page_size(request)

		if page_size is not None:
			self.paginate_by = page_size

		return super().get(request, *args, **kwargs)

