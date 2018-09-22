from django import template
from ..models.students import Student
from ..models.groups import Group
from ..models.logentry import LogEntry
 
register = template.Library()


@register.inclusion_tag('../templates/students/pagination.html')
def render_pagination(objects):

	if isinstance(objects[0], Student):
		return {
			"objects"          : objects,
			"first_page"       : "home",
			"default_order_by" : "last_name"
		}

	if isinstance(objects[0], Group):
		return {
			"objects"          : objects,
			"first_page"       : "groups",
			"default_order_by" : "title"
		}

	if isinstance(objects[0], LogEntry):
		return {
			"objects"          : objects,
			"first_page"       : "logs",
			"default_order_by" : "date"
		}

     