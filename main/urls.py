from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('teams/', views.TeamList.as_view(), name='team_list'),
    path('projects/', views.ProjectList.as_view(), name='project_list'),
    path('users/', views.UserList.as_view(), name='user_list'),

    path('new_team/', views.TeamFormView.as_view(), name='team_form'),
    path('new_project/', views.ProjectFormView.as_view(), name='project_form'),
    path('new_issue/', views.IssueFormView.as_view(), name='issue_form'),

    path('user/<str:username>', views.UserDetail.as_view(), name='user_detail'),

    path('t/<str:team_namespace>/', views.TeamDetail.as_view(), name='team_detail'),
    path('t/<str:team_namespace>/delete', views.TeamDelete.as_view(), name='team_delete'),
    path('t/<str:team_namespace>/p/<str:project_namespace>/',
         views.ProjectDetail.as_view(), name='project_detail'),
     path('t/<str:team_namespace>/p/<str:project_namespace>/delete',
         views.ProjectDelete.as_view(), name='project_delete'),
    path('p/<str:team_namespace>/<str:project_namespace>/issue/<int:issue_id>/',
         views.IssueDetail.as_view(), name='issue_detail'),
    path('p/<str:team_namespace>/<str:project_namespace>/issue/<int:issue_id>/delete',
         views.IssueDelete.as_view(), name='issue_delete'),
    path('p/<str:team_namespace>/<str:project_namespace>/issue/<int:issue_id>/edit',
         views.IssueEdit.as_view(), name='issue_edit'),

    path('t/<str:team_namespace>/new_project',
         views.ProjectFormView.as_view(), name='project_form'),
    path('t/<str:team_namespace>/p/<str:project_namespace>/new_issue',
         views.IssueFormView.as_view(), name='issue_form'),
]
