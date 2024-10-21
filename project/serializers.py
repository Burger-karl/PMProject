# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Project

# User = get_user_model()

# class ProjectSerializer(serializers.ModelSerializer):
#     assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
#     created_by = serializers.CharField(source='created_by.username', read_only=True)

#     class Meta:
#         model = Project
#         fields = ['id', 'name', 'description', 'assigned_to', 'created_by', 'date_created', 'status', 'priority']

#     def create(self, validated_data):
#         project = Project.objects.create(**validated_data)
#         return project

#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description', instance.description)
#         instance.assigned_to = validated_data.get('assigned_to', instance.assigned_to)
#         instance.status = validated_data.get('status', instance.status)
#         instance.priority = validated_data.get('priority', instance.priority)
#         instance.save()
#         return instance

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'user_type']








from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Project

User = get_user_model()

class ProjectSerializer(serializers.ModelSerializer):
    assigned_to = serializers.CharField(source='assigned_to.username', read_only=True)
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'assigned_to', 'created_by', 'date_created', 'status', 'priority']

    # Custom validation to ensure required fields
    def validate(self, data):
        if not data.get('name'):
            raise serializers.ValidationError("Project name is required.")
        if not data.get('description'):
            raise serializers.ValidationError("Project description is required.")
        if data.get('status') not in ['pending', 'in_progress', 'completed']:
            raise serializers.ValidationError("Invalid status. Choose from 'pending', 'in_progress', 'completed'.")
        if data.get('priority') not in ['low', 'medium', 'high']:
            raise serializers.ValidationError("Invalid priority. Choose from 'low', 'medium', 'high'.")
        return data

    def create(self, validated_data):
        try:
            project = Project.objects.create(**validated_data)
            return project
        except Exception as e:
            raise serializers.ValidationError(f"Error creating project: {str(e)}")

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.status = validated_data.get('status', instance.status)
        instance.priority = validated_data.get('priority', instance.priority)
        
        try:
            instance.save()
            return instance
        except Exception as e:
            raise serializers.ValidationError(f"Error updating project: {str(e)}")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'user_type']
