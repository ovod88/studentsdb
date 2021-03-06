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
from django.contrib.auth import views as auth_views

from django.urls import re_path as path
from django.conf.urls.static import static
from django.urls import include
from students.views.students import *
from students.views.groups import *
from students.views.journal import *
from students.views.examins import *
from students.views.professors import *
from students.views.studentList import *
from students.views.examins_results import *
from students.views.contact_admin import *
from students.views.logsList import *

from .settings import MEDIA_ROOT, MEDIA_URL, DEBUG

from django.views.generic import TemplateView, RedirectView
from students_auth.views import RegistrationView, ProfileUpdateView
from django.views.i18n import JavaScriptCatalog
from students.views.contact_admin_forms import ContactFormView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required

js_info_dict = {
    'packages': ('students',),
}

urlpatterns = [
    path('admin/', admin.site.urls),

    path(r'^users/profile/edit$', login_required(ProfileUpdateView.as_view()), name='profile_edit'),
    path(r'^users/profile/$', login_required(TemplateView.as_view(template_name='registration/profile.html')), name='profile'),
    
    path(r'^users/logout/$', auth_views.logout, kwargs={'next_page': 'home'}, name='auth_logout'),
    
    path(r'^register/complete/$', RedirectView.as_view(pattern_name='home'), name='registration_complete'),
    path(r'^users/register/$', RegistrationView.as_view(), name='registration_register'),
    
    path(r'^users/password/reset/$', auth_views.PasswordResetView.as_view(template_name='registration/auth_password_reset_form.html'), name='password_reset'),
    path(r'^reset/done/$', auth_views.PasswordResetDoneView.as_view(template_name='registration/auth_password_reset_done.html'), name='password_reset_done'),
    
    path(r'^reset/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path(r'^password/reset/complete/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path(r'^users/password/change/done/$', RedirectView.as_view(pattern_name='profile'), name='password_change_done'),
    
    # path(r'^users/', include('registration.backends.simple.urls')),#SIMPLE AUTHENTICATION
    path(r'^users/', include('registration.backends.default.urls')),#WITH EMAIL ACTIVATION AUTHENTICATION

    path('^social/', include('social.apps.django_app.urls', namespace='social')),

    path(r'^$', students_list3, name='home'),
    path(r'^students/add$', students_add, name='students_add'),#COMPLETELY MANUAL FORM
    # path(r'^students/add$', StudentCreateView.as_view(), name='students_add'),#CBV solution
    path(r'^students/(?P<pk>\d+)/edit$', StudentUpdateView.as_view(), name='students_edit'),
    path(r'^students/(?P<pk>\d+)/delete$', StudentDeleteView.as_view(), name='students_delete'),
    path(r'^students/delete$', StudentDeleteMultipleView.as_view(), name='students_multi_delete'),

    path(r'^students$', StudentList.as_view(), name='home_view'),

    path(r'^groups$', login_required(groups_list), name='groups'),
    path(r'^groups/add$', groups_add, name='groups_add'),
    path(r'^groups/(?P<gid>\d+)/edit$', groups_edit, name='groups_edit'),
    path(r'^groups/(?P<gid>\d+)/delete$', groups_delete, name='groups_delete'),

    path(r'^journal$', permission_required('auth.add_user')(journal_list), name='journal'),
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

    path(r'^logs$', LogsList.as_view(), name='logs'),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog')
] 

if DEBUG:
    urlpatterns += static(MEDIA_URL, document_root=MEDIA_ROOT)
