from django.test import TestCase
from django.http import HttpRequest

from students.groups_context import groups_context_processor


class ContextProcessorsTests(TestCase):

    fixtures = ['fixture_data.json']

    def test_groups_processor(self):
        """Test groups processor"""
        request = HttpRequest()
        data = groups_context_processor(request)

        # test data from processor
        self.assertEqual(len(data['GROUPS_ALL']), 4)
        self.assertEqual(data['GROUPS_ALL'][0]['str'], u'MTM-111 (Lina Khrystenko)')
        self.assertEqual(data['GROUPS_ALL'][1]['str'], u'MTM-12 (Roman2 Demo)')
