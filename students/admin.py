from django.contrib import admin
from .models.students import Student
from .models.groups import Group
from .models.journals import Journal
from .models.professors import Professor
from .models.examins import Examin
from .models.examins_results import ExaminResult
from django import forms



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


# Register your models here.
admin.site.register(Student)
admin.site.register(Group)
admin.site.register(Professor)
admin.site.register(Examin)
admin.site.register(ExaminResult, ExaminResultAdmin)