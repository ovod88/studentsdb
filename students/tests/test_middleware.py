from studentsdb.middleware import RequestTimeMiddleware
from django.test import TestCase, RequestFactory
from django.http import HttpRequest, HttpResponse
from django.urls import reverse
from ..views.students import students_list3
from students.models.students import Student

class MiddlewareTests(TestCase):

	fixtures = ['fixture_data.json']

	def setUp(self):
		self.client = RequestFactory(defaults={})

	def test_mymiddleware(self):
		request = self.client.request(request={})
		middle = RequestTimeMiddleware(students_list3)

		response = middle(request)

		self.assertTrue(request.end_time)
		self.assertTrue(request.start_time)

		self.assertIn('Request took', str(response.content))
		self.assertContains(response, 'student-edit-form-link', 12)

		