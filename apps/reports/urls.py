from django.urls import path
from . import views
app_name = 'reports'
urlpatterns = [
    path('',               views.report_list,   name='list'),
    path('new/',           views.report_create, name='create'),
    path('<str:pk>/edit/', views.report_edit,   name='edit'),
    path('<str:pk>/submit/', views.report_submit, name='submit'),
]
