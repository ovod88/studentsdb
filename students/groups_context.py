from .models.groups import Group
from .utils import get_groups

def groups_context_processor(request):

	return {'GROUPS_ALL' : get_groups(request)}