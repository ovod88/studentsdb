from setuptools import find_packages, setup

setup(
    name='django-studentsdb-app',
    version='1.0',
    author=u'Vova Khrystenko',
    author_email='ovod88@bigmir.net',
    packages=find_packages(),
    license='BSD licence, see LICENCE.txt',
    description='Students DB application',
    long_description=open('README.txt').read(),
    zip_safe=False,
    include_package_data=True,
    package_data = {
        'students': ['requirements.txt']
    },
)