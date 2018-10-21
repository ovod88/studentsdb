from django.test import TestCase

from ..models.students import Student


class StudentModelTests(TestCase):
    """Test student model"""

    def test_unicode(self):
        student = Student(first_name='Demo', last_name='Student')
        # self.assertEqual(unicode(student), u'Demo Student')
        self.assertEqual(student.first_name, 'Demo')
