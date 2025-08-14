from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.homeView, name='fhome'),
    path('domain/', views.domainView, name='fdomain'),
    path('project/', views.viewProject, name='fviewProject'),
    path('myprojects/', views.myProjects, name='fmyProjects'),
    path('gradeProject/', views.gradeProject, name='grade-project'),
    path('groupRequest/', views.requestView, name='frequest'),
]
