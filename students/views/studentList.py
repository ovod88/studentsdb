from django.views.generic import ListView
from students.models.students import Student

class StudentList(ListView):
	model = Student
	context_object_name = 'students'
	template_name = 'students/student_class_based_view_template.html'

	def get_context_data(self, **kwargs):
		context = super(StudentList, self).get_context_data(**kwargs)
		context['show_logo'] = False

		return context

	def get_queryset(self):
		qs = super(StudentList, self).get_queryset()

		return qs.order_by('last_name')