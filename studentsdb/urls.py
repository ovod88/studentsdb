"""studentsdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path as path
from django.conf.urls.static import static
from students.views.students import *
from students.views.groups import *
from students.views.journal import *
from students.views.examins import *
from students.views.professors import *
from students.views.examins_results import *
from students.views.contact_admin import *

from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG

from django.views.generic import TemplateView
from students.views.contact_admin_forms import ContactFormView

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^$', students_list3, name='home'),
    path(r'^students/add$', students_add, name='students_add'),#COMPLETELY MANUAL FORM
    path(r'^students/(?P<sid>\d+)/edit$', students_edit, name='students_edit'),
    path(r'^students/(?P<sid>\d+)/delete$', students_delete, name='students_delete'),

    path(r'^groups$', groups_list, name='groups'),
    path(r'^groups/add$', groups_add, name='groups_add'),
    path(r'^groups/(?P<gid>\d+)/edit$', groups_edit, name='groups_edit'),
    path(r'^groups/(?P<gid>\d+)/delete$', groups_delete, name='groups_delete'),

    path(r'^journal$', journal_list, name='journal'),
    path(r'^journal/(?P<sid>\d+)$', journal_student, name='journal_student'),

    path(r'^examins$', examins_list, name='examins'),
    path(r'^examins/(?P<eid>\d+)/edit$', examins_edit, name='examins_edit'),
    path(r'^examins/add$', examins_add, name='examins_add'),
    path(r'^examins/(?P<eid>\d+)/delete$', examins_delete, name='examins_delete'),

    path(r'^professors$', professors_list, name='professors'),
    path(r'^professors/(?P<pid>\d+)/edit$', professors_edit, name='professors_edit'),

    path(r'^examins_results$', examins_results_list, name='examins_results_list'),
    path(r'^examins_results/add$', examins_results_add, name='examins_results_add'),
    path(r'^examins_results/(?P<erid>\d+)/edit$', examins_results_edit, name='examins_results_edit'),
    path(r'^examins_results/(?P<erid>\d+)/delete$', examins_results_delete, name='examins_results_delete'),

    path(r'^contact_admin$', contact_admin, name='contact_admin'),#FORM USING DJANGO FORMS

    path(r'^contact_admin_forms$', ContactFormView.as_view(), name='contact_admin_forms'),#FORM USING DJANGO CONTACT FORM
    path(r'^contact_admin_forms/sent/$', TemplateView.as_view(template_name='contact_admin_forms/contact_form_sent.html'),
                            name='contact_admin_forms_sent'),
] 

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
