from django.urls import path
from . import views

app_name = 'evidence'
urlpatterns = [
    path('',                                   views.evidence_list,          name='list'),
    path('scan/',                              views.barcode_lookup,          name='barcode_lookup'),
    path('new/',                               views.evidence_create,         name='create'),
    path('<str:pk>/detail/',                  views.evidence_detail,         name='detail'),
    path('<str:pk>/edit/',                    views.evidence_edit,           name='edit'),
    path('<str:evidence_pk>/test/new/',       views.labtest_create,          name='labtest_create'),
    path('test/<str:pk>/results/',            views.labtest_enter_results,   name='labtest_results'),
    path('test/<str:pk>/edit/',              views.labtest_edit,             name='labtest_edit'),
]
