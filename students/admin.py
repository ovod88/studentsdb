from django.contrib import admin
from .models.students import Student
from .models.groups import Group
from .models.journals import Journal
from .models.professors import Professor
from .models.examins import Examin
from .models.examins_results import ExaminResult
from django import forms
from django.urls import reverse



class ExaminResultForm(forms.ModelForm):
	class Meta:
		model=ExaminResult
		fields = '__all__'

	def clean(self):
		data = self.cleaned_data
		student = data.get('student')
		examin = data.get('examin')

		if student.student_group != examin.examin_group:
			raise forms.ValidationError('Group mismatch between examin and student!')

		return data


class ExaminResultAdmin(admin.ModelAdmin):
	form = ExaminResultForm

class StudentAdmin(admin.ModelAdmin):
	list_display = ['last_name', 'first_name', 'ticket', 'student_group']
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 10
	search_fields = ['last_name', 'first_name', 'middle_name', 'ticket','notes']
	actions = ['copy_selected']

	def copy_selected(self, request, queryset):
		# print(queryset)
		# print(self)
		# print(request.POST)
		for student in queryset:
			student.pk = None
			student.save()
		self.message_user(request, "%s successfully copied in database." % len(queryset))
	copy_selected.short_description = "Copy selected students"

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk': obj.id})

# Register your models here.
admin.site.register(Student, StudentAdmin)
admin.site.register(Group)
admin.site.register(Professor)
admin.site.register(Examin)
admin.site.register(ExaminResult, ExaminResultAdmin)