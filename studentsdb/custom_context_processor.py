from .settings import LANGUAGES_SUPPORTED, LANGUAGE_CODE
from .utils import get_language
from django.utils import translation

def students_proc(request):
	
	return {'PORTAL_URL': request.build_absolute_uri('/')[:-1]}

def set_language(request):
	languages = []
	language_cookie = get_language(request)
	if language_cookie and language_cookie in LANGUAGES_SUPPORTED:

		translation.activate(language_cookie)
		
		for language in LANGUAGES_SUPPORTED:
			languages.append({
				'name': language,
				'selected': language == language_cookie
			})
		languages.append({
				'name': LANGUAGE_CODE,
				'selected': False
			})
	else:
		for language in LANGUAGES_SUPPORTED:
			languages.append({
				'name': language,
				'selected': False
			})
		languages.append({
				'name': LANGUAGE_CODE,
				'selected': True
			})

	return {'LANGUAGES': languages}
