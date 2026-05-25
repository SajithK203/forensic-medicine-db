from django.urls import path
from . import views
app_name = 'staff'
urlpatterns = [
    path('',               views.staff_list,    name='list'),
    path('new/',           views.staff_create,  name='create'),
    path('<str:pk>/edit/', views.staff_edit,    name='edit'),
    path('doctors/new/',   views.doctor_create, name='doctor_create'),
]
