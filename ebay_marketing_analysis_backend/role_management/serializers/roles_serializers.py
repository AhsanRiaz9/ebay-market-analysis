from role_management.models import Role, Permission, Module
from rest_framework import serializers
from .permissions_serializers import (
    PermissionSerializer,
    ModulePermissionSerializer,
)
from rest_framework.exceptions import ValidationError


class RoleSerializer(serializers.ModelSerializer):
    modules = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = ["id", "name", "modules"]

    def get_modules(self, obj):
        modules = Module.objects.filter(
            permissions__in=obj.permissions.all()
        ).distinct()
        return ModulePermissionSerializer(
            modules, many=True, context={"role": obj}
        ).data


class RoleCreateSerializer(serializers.ModelSerializer):
    permissions = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Permission.objects.all()
    )

    class Meta:
        model = Role
        fields = ["name", "permissions"]
        depth = 1
