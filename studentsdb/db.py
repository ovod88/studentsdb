
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
#This one is for sqlite db
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR,'..', 'db.sqlite3'),
#     }
# }

#This one is for MySQL
DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'HOST'     : 'localhost',
        'USER'     : 'students_db_user',
        'PASSWORD' : 'taon8888',
        'NAME'     : 'students_db',
        'TEST': {
        	'NAME': 'test_students_db', 
			'CHARSET': 'utf8',
			'COLLATION': 'utf8_general_ci',
		}
    }
}

#This one is for PostgreSQL
# DATABASES = {
#     'default': {
#         'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
#         'HOST'     : 'localhost',
#         'USER'     : 'students_db_user',
#         'PASSWORD' : 'taon8888',
#         'NAME'     : 'students_db',
#     }
# }