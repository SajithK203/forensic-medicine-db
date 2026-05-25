from django.urls import path
from . import views
app_name = 'evidence'
urlpatterns = [
    path('',                          views.evidence_list,   name='list'),
    path('new/',                      views.evidence_create, name='create'),
    path('<str:pk>/edit/',            views.evidence_edit,   name='edit'),
    path('<str:evidence_pk>/test/new/', views.labtest_create, name='labtest_create'),
]
