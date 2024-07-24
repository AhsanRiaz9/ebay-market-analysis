from role_management.models import Permission
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from role_management.paginator import CustomPagination
from role_management.serializers import PermissionSerializer, ModuleSerializer
from rest_framework.response import Response
from role_management.permissions import HasPermission
from rest_framework.permissions import IsAuthenticated


class PermissionAPIView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_permissions"
        elif self.request.method == "POST":
            required_permission_code = "add_permissions" 
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request):
        permission = Permission.objects.all()
        serializers = PermissionSerializer(permission, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = PermissionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Permission created successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PermissionObjectView(APIView):
    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_permissions"
        elif self.request.method == "PUT":
            required_permission_code = "update_permissions"
        elif self.request.method == "DELETE":
            required_permission_code = "delete_permissions"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request, permission_id):
        permission = get_object_or_404(Permission, id=permission_id)
        serializers = PermissionSerializer(permission)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, permission_id):
        permission = get_object_or_404(Permission, id=permission_id)
        serializers = PermissionSerializer(permission, data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(
                {"message", "Permission Updated Successfully"},
                status=status.HTTP_200_OK,
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, permission_id):
        permission = get_object_or_404(Permission, id=permission_id)
        permission.delete()
        return Response(
            {"message": "Permission Deleted Successfully"}, status=status.HTTP_200_OK
        )
