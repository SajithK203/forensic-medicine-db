from django.urls import path
from . import views
app_name = 'postmortem'
urlpatterns = [
    path('',           views.pm_list,   name='list'),
    path('new/',       views.pm_create, name='create'),
    path('<str:pk>/edit/', views.pm_edit, name='edit'),
]
