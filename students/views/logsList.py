from django.views.generic import ListView
from students.models.logentry import LogEntry

class LogsList(ListView):

	model = LogEntry
	context_object_name = 'logs'
	template_name = 'students/logs.html'
	queryset = LogEntry.objects.all().order_by('date')
	paginate_by = 10

	def get_context_data(self, **kwargs):

		page_size = super().get_paginate_by(self.queryset)
		context_object_name = self.get_context_object_name(self.queryset)

		if page_size:
			paginator, logs_page, logs, if_paginated = super().paginate_queryset(self.queryset, page_size)
			context = {
				'objects' : logs_page
			}
		else:
			context = {
				'objects' : None
			}

		context.update(kwargs)

		if context_object_name is not None:
			context[context_object_name] = self.queryset
		return context
