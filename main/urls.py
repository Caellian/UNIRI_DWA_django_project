from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('teams/', views.TeamList.as_view(), name='team_list'),
    path('projects/', views.ProjectList.as_view(), name='project_list'),
    path('users/', views.UserList.as_view(), name='user_list'),

    path('user/<str:username>', views.UserDetail.as_view(), name='user_detail'),

    path('<str:team_namespace>/', views.TeamDetail.as_view(), name='team_detail'),
    path('<str:team_namespace>/<str:project_namespace>/',
         views.ProjectDetail.as_view(), name='project_detail'),
    path('<str:team_namespace>/<str:project_namespace>/issue/<int:issue_id>/',
         views.IssueDetail.as_view(), name='issue_detail'),
]
