from django.views.generic import ListView
from students.models.logentry import LogEntry

class LogsList(ListView):

	model = LogEntry
	context_object_name = 'logs'
	template_name = 'students/logs.html'

	def get_queryset(self):
		qs = super().get_queryset()

		return qs.order_by('date')