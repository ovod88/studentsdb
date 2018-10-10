from os.path import basename, relpath, normpath
import os
from .settings import BASE_DIR

def getMobuleProjectPath(fullpath):
	path_str = str(relpath(normpath(fullpath), BASE_DIR)).split('.')[:-1][0]
	path_str = path_str.replace(os.sep, '.')

	return path_str

def get_language(request):
	cookie_value = request.COOKIES.get('language')

	if cookie_value:
		return cookie_value
	else:
		return None