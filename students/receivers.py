import logging

from django.db.models.signals import post_save, post_delete, post_migrate
from django.core.signals import request_started
from django.dispatch import receiver

from .models.students import Student
from .models.groups import Group
from .signals import email_admin_sent_signal

logger = logging.getLogger(__name__)
request_counter = 0

@receiver(post_save, sender=Group)
@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):

	if sender.__name__ == 'Student':
		student = kwargs['instance']

		if kwargs['created']:
			logger.info('Student added: %s %s (ID: %d)', student.first_name,
							student.last_name, student.id)
		else:
			logger.info('Student updated: %s %s (ID: %d)', student.first_name,
							student.last_name, student.id)
	elif sender.__name__ == 'Group':
		group = kwargs['instance']

		if kwargs['created']:
			logger.info('Group added: %s (leader: %s %s)', group.title, 
							group.leader.first_name, group.leader.last_name)
		else:
			logger.info('Group updated: %s (leader: %s %s)', group.title, 
							group.leader.first_name, group.leader.last_name)

@receiver(post_delete, sender=Student)
def log_student_deleted_event(sender, **kwargs):

	student = kwargs['instance']
	logger.info('Student deleted: %s %s (ID: %d)', student.first_name,
					student.last_name, student.id)


@receiver(email_admin_sent_signal, sender=None)
def email_admin_sent(sender, **kwargs):

	from_who = kwargs['from_']
	message = kwargs['message']
	logger.info('Message was sent successfully from %s with message: %s', from_who, message)

@receiver(post_migrate)
def post_migrate(sender, **kwargs):

	print(kwargs['using'])

@receiver(request_started)
def request_started(sender, **kwargs):

	global request_counter
	request_counter += 1
	# print(request_counter)