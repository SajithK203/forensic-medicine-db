from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('accounts/',   include('apps.accounts.urls')),
    path('patients/',   include('apps.patients.urls')),
    path('cases/',      include('apps.cases.urls')),
    path('clinical/',   include('apps.clinical.urls')),
    path('postmortem/', include('apps.postmortem.urls')),
    path('evidence/',   include('apps.evidence.urls')),
    path('reports/',    include('apps.reports.urls')),
    path('staff/',      include('apps.staff.urls')),
    path('',            include('apps.core.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site branding
admin.site.site_header = 'Forensic Medicine DB — Admin'
admin.site.site_title  = 'FMD Admin'
admin.site.index_title = 'Administration Panel'