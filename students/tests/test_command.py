from django.core.management import call_command
from django.test import TestCase
from django.utils.six import StringIO


class STCountTest(TestCase):
    """Test stcount command"""

    fixtures = ['fixture_data.json']

    def test_command_output(self):
        # prepare output file for command
        out = StringIO()

        # call our command
        call_command('stcount', 'student', stdout=out)

        # get command output
        result = out.getvalue()

        # check if we get proper number of objects in database
        self.assertIn('students in database: 20', result)
        # self.assertIn('groups in database: 2', result)
        # self.assertIn('users in database: 1', result)
