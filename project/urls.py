from django.urls import path
from . import views

urlpatterns = [
    # Admin urls
    path('projects/create/', views.ProjectCreateView.as_view(), name='project-create'),
    path('projects/update/<int:pk>/', views.ProjectUpdateView.as_view(), name='project-update'),
    path('projects/delete/<int:pk>/', views.ProjectDeleteView.as_view(), name='project-delete'),
    path('projects/assign/<int:pk>/', views.AssignProjectToClientView.as_view(), name='project-assign'),

    path('clients/', views.ClientListView.as_view(), name='client-list'),
    path('projects/', views.AllProjectsListView.as_view(), name='all-projects-list'),
    
    # for client
    path('my-projects/', views.ClientAssignedProjectsView.as_view(), name='client-assigned-projects'),
]
