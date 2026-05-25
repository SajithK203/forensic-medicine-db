from django.urls import path
from . import views
app_name = 'cases'
urlpatterns = [
    path('',                     views.case_list,          name='list'),
    path('new/',                 views.case_create,        name='create'),
    path('<str:pk>/',            views.case_detail,        name='detail'),
    path('<str:pk>/edit/',       views.case_edit,          name='edit'),
    path('<str:pk>/status/',     views.case_update_status, name='update_status'),
]
