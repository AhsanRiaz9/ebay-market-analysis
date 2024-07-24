from role_management.models import Permission, Module
from rest_framework import serializers
from .modules_serializers import ModuleSerializer
from rest_framework.exceptions import ValidationError


class PermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = "__all__"


class ShowPermissionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Permission
        fields = ["id", "name", "code"]


class ModulePermissionSerializer(serializers.ModelSerializer):
    permissions = serializers.SerializerMethodField()

    class Meta:
        model = Module
        fields = ["id", "name", "permissions"]

    def get_permissions(self, obj):
        role = self.context["role"]
        permissions = role.permissions.filter(module=obj)
        return ShowPermissionSerializer(permissions, many=True).data


class ModuleWithPermissionSerializer(serializers.ModelSerializer):
    permissions = ShowPermissionSerializer(many=True, read_only=True)

    class Meta:
        model = Module
        fields = ["id", "name", "permissions"]
