from django.urls import path
from . import views
app_name = 'clinical'
urlpatterns = [
    path('',           views.exam_list,   name='list'),
    path('new/',       views.exam_create, name='create'),
    path('<str:pk>/edit/', views.exam_edit, name='edit'),
]
