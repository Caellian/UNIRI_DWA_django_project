from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('projects/', views.ProjectListView.as_view(), name='project_list'),
    path('projects/<uuid:project_id>', views.ProjectDetailView.as_view(), name='project_detail'),
    path('projects/create', views.ProjectFormCreateView.as_view(), name='project_create'),
]
