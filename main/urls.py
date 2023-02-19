from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.Dashboard.as_view(), name='dashboard'),
    path('teams/', views.TeamList.as_view(), name='team_list'),
    path('projects/', views.ProjectList.as_view(), name='project_list'),
    path('issues/', views.IssueList.as_view(), name='issue_list'),
    path('users/', views.UserList.as_view(), name='user_list'),
    path('comments/', views.CommentList.as_view(), name='comment_list'),
    #path('projects/<uuid:project_id>', views.ProjectDetailView.as_view(), name='project_detail'),

]
