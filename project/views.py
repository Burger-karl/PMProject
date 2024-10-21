from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .models import Project
from .serializers import ProjectSerializer, UserSerializer
from rest_framework.exceptions import NotFound, ValidationError
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()

class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class ProjectCreateView(generics.CreateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="Create a new project",
        operation_description="Admin users can create a new project with name, description, etc.",
        responses={201: ProjectSerializer, 400: "Bad request"},
    )
    def perform_create(self, serializer):
        try:
            serializer.save(created_by=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred while creating the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectUpdateView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="Update a project",
        operation_description="Admin users can update an existing project with new data.",
        responses={200: ProjectSerializer, 400: "Bad request"},
    )
    def perform_update(self, serializer):
        try:
            serializer.save()
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": "An error occurred while updating the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ProjectDeleteView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="Delete a project",
        operation_description="Admin users can delete a project by ID.",
        responses={204: "No content", 500: "Internal server error"},
    )
    def perform_destroy(self, instance):
        try:
            instance.delete()
        except Exception as e:
            return Response({"error": "An error occurred while deleting the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ClientListView(generics.ListAPIView):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="List all clients",
        operation_description="Admin users can view all registered clients (non-admin users).",
        responses={200: UserSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class ClientAssignedProjectsView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="View assigned projects for a client",
        operation_description="Clients can view all projects assigned to them.",
        responses={200: ProjectSerializer(many=True)}
    )
    def get_queryset(self):
        return Project.objects.filter(assigned_to=self.request.user)


class AllProjectsListView(generics.ListAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin]

    @swagger_auto_schema(
        operation_summary="View all projects (Admin only)",
        operation_description="Admin users can view all projects in the system.",
        responses={200: ProjectSerializer(many=True)}
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)


class AssignProjectToClientView(generics.UpdateAPIView):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [IsAdmin]
    lookup_field = 'pk'

    @swagger_auto_schema(
        operation_summary="Assign project to a client",
        operation_description="Admin can assign a project to a client using the client's username.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Username of the client'),
            },
        ),
        responses={200: "Project assigned successfully", 404: "Client not found", 400: "Bad request"}
    )
    def update(self, request, *args, **kwargs):
        project = self.get_object()
        username = request.data.get('username')

        if not username:
            return Response({'error': "Username is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound(f"Client with username '{username}' not found.")
        except Exception as e:
            return Response({"error": "An error occurred while assigning the project."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        project.assigned_to = user
        project.save()

        return Response({
            'message': f"Project '{project.name}' has been assigned to {user.username}.",
            'project': ProjectSerializer(project).data
        }, status=status.HTTP_200_OK)
