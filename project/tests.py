from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class ProjectTests(APITestCase):

    def setUp(self):
        # Create a test admin user and a test client user
        self.admin_user = User.objects.create_user(username='admin', password='admin123', is_staff=True)
        self.client_user = User.objects.create_user(username='client', password='client123')
        
        self.client = APIClient()
        self.admin_client = APIClient()
        
        # Admin client authenticates
        self.admin_client.login(username='admin', password='admin123')
        
        # Create a test project
        self.project = Project.objects.create(name='Test Project', created_by=self.admin_user)
    
    def test_project_create_view(self):
        """ Test project creation by admin """
        url = reverse('project-create')
        data = {'name': 'New Project'}
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Project.objects.count(), 2)
        self.assertEqual(Project.objects.get(name='New Project').created_by, self.admin_user)

    def test_project_create_view_unauthorized(self):
        """ Test that non-admin users cannot create a project """
        self.client.login(username='client', password='client123')
        url = reverse('project-create')
        data = {'name': 'New Project'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_update_view(self):
        """ Test project update by admin """
        url = reverse('project-update', kwargs={'pk': self.project.pk})
        data = {'name': 'Updated Project'}
        response = self.admin_client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.name, 'Updated Project')

    def test_project_update_view_unauthorized(self):
        """ Test that non-admin users cannot update a project """
        self.client.login(username='client', password='client123')
        url = reverse('project-update', kwargs={'pk': self.project.pk})
        data = {'name': 'Unauthorized Update'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_project_delete_view(self):
        """ Test project deletion by admin """
        url = reverse('project-delete', kwargs={'pk': self.project.pk})
        response = self.admin_client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Project.objects.filter(pk=self.project.pk).exists())

    def test_project_delete_view_unauthorized(self):
        """ Test that non-admin users cannot delete a project """
        self.client.login(username='client', password='client123')
        url = reverse('project-delete', kwargs={'pk': self.project.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_list_view(self):
        """ Test that admin can view all clients """
        url = reverse('client-list')
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only one client user

    def test_client_list_view_unauthorized(self):
        """ Test that non-admin users cannot view client list """
        self.client.login(username='client', password='client123')
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_client_assigned_projects_view(self):
        """ Test that client can view their assigned projects """
        # Assign the project to the client user
        self.project.assigned_to = self.client_user
        self.project.save()

        self.client.login(username='client', password='client123')
        url = reverse('client-assigned-projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_client_assigned_projects_view_no_permission(self):
        """ Test that non-authenticated users cannot view assigned projects """
        url = reverse('client-assigned-projects')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_all_projects_list_view(self):
        """ Test that admin can view all projects """
        url = reverse('all-projects-list')
        response = self.admin_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), Project.objects.count())

    def test_all_projects_list_view_unauthorized(self):
        """ Test that non-admin users cannot view all projects """
        self.client.login(username='client', password='client123')
        url = reverse('all-projects-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_assign_project_to_client_view(self):
        """ Test that admin can assign a project to a client """
        url = reverse('assign-project-to-client', kwargs={'pk': self.project.pk})
        data = {'username': self.client_user.username}
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.assigned_to, self.client_user)

    def test_assign_project_to_client_view_invalid_client(self):
        """ Test assigning project to a non-existent client """
        url = reverse('assign-project-to-client', kwargs={'pk': self.project.pk})
        data = {'username': 'non_existent_user'}
        response = self.admin_client.patch(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
