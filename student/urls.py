from django.urls import path
from . import views

urlpatterns = [
    path('', views.homeView, name='shome'),
    path('timeline/', views.timelineView, name='timeline'),
    path('group/', views.groupView, name='groupmate'),
    path('domain/', views.domainView, name='sdomain'),
    path('delete/', views.deleteMember, name='deleteMember'),
    path('project/', views.viewProject, name='viewProject'),
]