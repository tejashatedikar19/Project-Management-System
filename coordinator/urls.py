from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('setDeadline/', views.setDeadline, name='set-deadline'),
    path('downloadReport/', views.downloadReport, name='download-status'),
]
