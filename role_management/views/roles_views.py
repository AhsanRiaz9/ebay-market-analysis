from role_management.models import Role
from rest_framework import generics, status
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
# from role_management.paginator import CustomPagination
from role_management.serializers import RoleSerializer, RoleCreateSerializer
from rest_framework.response import Response
from role_management.permissions import HasPermission
from rest_framework.permissions import IsAuthenticated


class RoleAPIView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_role"
        elif self.request.method == "POST":
            required_permission_code = "add_role"
        
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request):
        role = Role.objects.exclude(name='superadmin')
        serializers = RoleSerializer(role, many=True)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializers = RoleCreateSerializer(data=request.data)
        print(serializers)
        print(serializers.is_valid())
        if serializers.is_valid():
            serializers.save()
            return Response(
                {"message": "Role Created Successfully."},
                status=status.HTTP_201_CREATED,
            )
        return Response({"error":"Role already exists"}, status=status.HTTP_400_BAD_REQUEST)


class RoleObjectView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_role"
        elif self.request.method == "PUT":
            required_permission_code = "update_role"
        elif self.request.method == "DELETE":
            required_permission_code = "delete_role"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializers = RoleSerializer(role)
        return Response(serializers.data ,status=status.HTTP_200_OK)

    def put(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        serializers = RoleCreateSerializer(role, data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                {"message": "Role Updated Successfully"}, status=status.HTTP_201_CREATED
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, role_id):
        role = get_object_or_404(Role, id=role_id)
        role.delete()
        return Response(
            {"message": "Role Deleted Successfully"}, status=status.HTTP_200_OK
        )
