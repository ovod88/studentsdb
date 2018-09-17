import logging

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models.students import Student
from .models.groups import Group

@receiver(post_save, sender=Group)
@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
	logger = logging.getLogger(__name__)

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
	logger = logging.getLogger(__name__)

	student = kwargs['instance']
	logger.info('Student deleted: %s %s (ID: %d)', student.first_name,
					student.last_name, student.id)