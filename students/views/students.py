from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.http import JsonResponse
from django.template import RequestContext, loader
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import datetime
from django.contrib import messages
from django.contrib.messages import get_messages
from django.views.generic import UpdateView, DeleteView, CreateView, FormView
from django.forms import *
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions
import os


from ..models.students import Student
from ..models.groups import Group
from PIL import Image
# from ..MyPaginator import MyPaginator, PageNotAnInteger, EmptyPage

import json
from django.views.decorators.csrf import csrf_exempt

def clear_messages(request):
	# list(messages.get_messages(request))#DOES THE SAME
	storage = get_messages(request)
	for message in storage:#removing all messages
		pass

def students_list3(request):
	# students = (
	# 	{'id': 1,
	# 	'first_name': u'Віталій',
	# 	'last_name': u'Подоба',
	# 	'ticket': 235,
	# 	'image': 'img/podoba3.jpg'},
	# 	{'id': 2,
	# 	'first_name': u'Корост',
	# 	'last_name': u'Андрій',
	# 	'ticket': 2123,
	# 	'image': 'img/me.jpeg'},
	# 	{'id': 3,
	# 	'first_name': u'Притула',
	# 	'last_name': u'Тарас',
	# 	'ticket': 5332,
	# 	'image': 'img/piv.png'}
	# 	)
	# students = Student.objects.all()
	
	# students = Student.students.all()

	students = Student.students.get_queryset().order_by('id')

	order = request.GET.get('order_by','')
	page = request.GET.get('page')
	reverse = request.GET.get('reverse', '')

	# def ticket_sorting(student):
	# 	return int(student.ticket)

	if order in ('first_name', 'last_name'):
		students = students.order_by(order)

		if reverse == '1':
			students = students.reverse()

		# if order == 'ticket':
		# 	students = sorted(students, key=ticket_sorting, reverse=int(request.GET.get('reverse', '0')))
	
	#JUST FOR TESTING. DO NOT DO SORTINTG IN PYTHON ON PRODUCTION!!!USE CORRECT TYPE FIELDS
	if order == 'ticket':
		# print('CALLED ORDER BY TICKET')
		if reverse == '':
			students = Student.students.all_with_ticket_sorted(0)
		else:
			students = Student.students.all_with_ticket_sorted(int(request.GET.get('reverse', '0')))

	# print('-----HERE------')
	# print(students)

	if (not request.GET or ((page is not None or page != '') and not order and not reverse)) or \
		(request.method == 'POST' and not request.POST):
		# print('CALLED DEFAULT ORDER')
		# print(type(students))
		students = students.order_by('last_name')

	#MY OWN REALISATION OF PAGINATOR
	# paginator = MyPaginator(students, 3)
	paginator = Paginator(students, 3)


	# print(request.GET)
	# print(request.POST)

	if request.method == 'GET':
		# print('HELLO GET')
		try:
			students = paginator.page(page)
		except PageNotAnInteger:
			# If page is not an integer, deliver first page.
			students = paginator.page(1)
		except EmptyPage:
			# If page is out of range (e.g. 9999), deliver
			# last page of results.
			students = paginator.page(paginator.num_pages)

	if request.method == 'POST':
		# print('HELLO POST')
		# print(order, reverse, page)
		# print(request.POST.get('load_more', False))
		# print(request.POST.get('ajax_page'))
		load_more = request.POST.get('load_more', False)
		ajax_page = request.POST.get('ajax_page')
		if ajax_page and load_more:

			ajax_page = int(ajax_page)
			if ajax_page <= paginator.num_pages:
				students = paginator.page(ajax_page)
			else:
				students = {}
		else:
			students = {}

		students_page = list(map(lambda student: student.as_dict(), students))

		return JsonResponse({'students': students_page})
	
	# import pdb;pdb.set_trace()
	return render(request, 'students/students_list.html', {'students': students})

def students_add(request):
	groups = Group.objects.order_by('id')

	if request.method == 'POST':
		if request.POST.get('add_button') is not None:
			#TODO VALIDATION HERE
			errors = {}

			data = {'middle_name': request.POST.get('middle_name'),
					'notes': request.POST.get('notes')}

			first_name = request.POST.get('first_name', '').strip()
			if not first_name:
				errors['first_name'] = u"Ім’я є обов’язковим"
			else:
				data['first_name'] = first_name

			last_name = request.POST.get('last_name', '').strip()
			if not last_name:
				errors['last_name'] = u"Прізвище є обов’язковим"
			else:
				data['last_name'] = last_name
			
			birthday = request.POST.get('birthday', '').strip()
			if not birthday:
				errors['birthday'] = u"Дата народження є обов’язковою"
			else:
				try:
					datetime.strptime(birthday, '%Y-%m-%d')
				except Exception:
					errors['birthday'] = u"Введіть коректний формат дати (напр. 1984-39 12-30)"
				else:
					data['birthday'] = birthday

			ticket = request.POST.get('ticket', '').strip()
			if not ticket:
				errors['ticket'] = u"Номер білета є обов’язковим"
			else:
				data['ticket'] = ticket

			student_group = request.POST.get('student_group', '').strip()
			if not student_group:
				errors['student_group'] = u"Оберіть групу для студента"
			else:
				groups_selected = Group.objects.filter(pk=student_group)
				if len(groups_selected) != 1:
					errors['student_group'] = u"Оберіть коректну групу"
				else:
					data['student_group'] = groups_selected[0]

			photo = request.FILES.get('photo')

			if photo:

				VALID_IMAGE_EXTENSIONS = [
	    			".jpg",
	    			".jpeg",
	    			".png",
	    			".gif",
				]

				if not any([str(photo).lower().endswith(e) for e in VALID_IMAGE_EXTENSIONS]):
					errors['photo'] = 'Not a valid image extension (supported jpg, jpeg, png, gif)'
				elif photo._size > 2097152:
					errors['photo'] = 'Please upload image smaller than 2mB'
				else:
					try:
						im=Image.open(photo).verify()
					except IOError as e:
						errors['photo'] = 'Not a valid image file'
					else:
						data['photo'] = photo			

			if not errors:
				student = Student(**data)
				student.save()

				clear_messages(request)

				messages.success(request, 'Студента %s успішно додано' % student)

				return HttpResponseRedirect(reverse('home'))
				# return HttpResponseRedirect(u'%s?status_message=Студента %s успішно додано!' % (reverse('home'), student))
			
			else:
				clear_messages(request)

				messages.error(request, 'Будь-ласка, виправте наступні помилки')

				return render(request, 'students/students_add.html', {
					'errors' : errors,
					'groups' : groups
				})
		elif request.POST.get('cancel_button') is not None:
			# redirect to home page on cancel button
			clear_messages(request)

			messages.info(request, 'Додавання студента скасовано!')

			return HttpResponseRedirect(reverse('home'))
			# return HttpResponseRedirect(u'%s?status_message=Додавання студента скасовано!' % reverse('home'))
	
	return render(request, 'students/students_add.html', {'groups' : groups})

# def students_edit(request, sid):
# 	return HttpResponse(f'<h1>Edit Student {sid}</h1>')


class StudentUpdateForm(ModelForm):
	class Meta:
		model = Student
		exclude=['student_examin']
	
	def __init__(self, *args, **kwargs):
		super(StudentUpdateForm, self).__init__(*args, **kwargs)

		self.helper = FormHelper(self)

		# set form tag attributes
		if hasattr(kwargs['instance'], 'id'):
			self.helper.form_action = reverse('students_edit', kwargs={'pk': kwargs['instance'].id})
		else:
			self.helper.form_action = reverse('students_add')
		self.helper.form_method = 'POST'
		self.helper.form_class = 'form-horizontal'

		# set form field properties
		self.helper.help_text_inline = True
		self.helper.html5_required = True
		self.helper.label_class = 'col-sm-2 control-label'
		self.helper.field_class = 'col-sm-10'
		# add buttons

		self.helper.add_input(Submit('add_button', u'Зберегти', css_class="btn btn-primary"))
		self.helper.add_input(Submit('cancel_button', u'Скасувати', css_class="btn btn-link",
										formnovalidate='formnovalidate'))

class StudentCreateView(CreateView):
	model=Student
	template_name='students/student_edit.html'
	form_class = StudentUpdateForm

	def get_success_url(self):

		clear_messages(self.request)

		messages.success(self.request, 'Студента %s успішно додано' % self.object)

		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			clear_messages(request)

			messages.info(request, 'Додавання студента скасовано!')

			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentCreateView, self).post(request, *args, **kwargs)

class StudentUpdateView(UpdateView):
	model=Student
	template_name='students/student_edit.html'
	form_class = StudentUpdateForm

	def get_success_url(self):

		clear_messages(self.request)

		messages.success(self.request, 'Студента %s успішно збережено!' % self.object)

		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			clear_messages(request)

			messages.info(request, 'Редагування студента відмінено!')

			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentUpdateView, self).post(request, *args, **kwargs)

# def students_delete(request, sid):
	# return HttpResponse(f'<h1>Delete Student {sid}</h1>')

class StudentDeleteView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_delete.html'
	context_object_name = 'student'

	def get_success_url(self):
		clear_messages(self.request)

		messages.info(self.request, 'Студента успішно видалено!')
		return reverse('home')

	def post(self, request, *args, **kwargs):
		if request.POST.get('cancel_button'):
			clear_messages(request)

			messages.info(request, 'Видалення студента відмінено!')

			return HttpResponseRedirect(reverse('home'))
		else:
			return super(StudentDeleteView, self).post(request, *args, **kwargs)

class StudentDeleteMultipleView(DeleteView):
	model = Student
	template_name = 'students/students_confirm_many_delete.html'
	context_object_name = 'list_of_students'


	def get_queryset(self):
		qs = super().get_queryset()
		list_id_of_students = self.request.GET.getlist('selected_students')
		# print(self.request.GET.getlist('selected_students'))
		# print(qs.filter(id__in=list_id_of_students))

		return qs.filter(id__in=list_id_of_students)

	def get_object(self, queryset=None):
		obj = self.get_queryset()
		
		return obj

	def delete(self, request, *args, **kwargs):
	    if self.request.POST.get('delete_button') is not None:
	        list_id_of_students = request.POST.getlist('selected_students')
	        # print(request.POST)
	        self.model.students.filter(id__in=list_id_of_students).delete()

	    #import pdb; pdb.set_trace();
	    return HttpResponseRedirect(self.get_success_url())

	def get_success_url(self):
	    #import pdb; pdb.set_trace()
	    clear_messages(self.request)

	    if self.request.POST.get('cancel_button') is not None:
	    	messages.warning(self.request, 'Видалення студентів відмінено!')
	    if self.request.POST.get('delete_button') is not None:
	    	messages.success(self.request, 'Студентів успішно видалено!')

	    return reverse('home')