from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from role_management.models import Module
from role_management.serializers import ModuleSerializer, ModuleWithPermissionSerializer
from role_management.permissions import HasPermission
from rest_framework.permissions import IsAuthenticated
from role_management.paginator import CustomPagination


class ModuleView(APIView):
    required_permission_code = "view_module"
    permission_classes = [IsAuthenticated, HasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        module = Module.objects.all()
        paginator = self.pagination_class()
        paginated_modules = paginator.paginate_queryset(module, request)

        serializers = ModuleWithPermissionSerializer(paginated_modules, many=True)
        return paginator.get_paginated_response(serializers.data)


class ModuleAPIView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_module"
        elif self.request.method == "POST":
            required_permission_code = "add_module"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        module = Module.objects.all()
        paginator = self.pagination_class()
        paginated_modules = paginator.paginate_queryset(module, request)

        serializers = ModuleSerializer(paginated_modules, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        serializer = ModuleSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Module Created Successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response({"error":"Module Already exists"}, status=status.HTTP_400_BAD_REQUEST)


class ModuleObjectView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_module"
        elif self.request.method == "DELETE":
            required_permission_code = "delete_module"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        serializer = ModuleSerializer(module)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, module_id):
        module = get_object_or_404(Module, id=module_id)
        module.delete()
        return Response(
            {"message": "Module Deleted Successfully."},
            status=status.HTTP_200_OK,
        )
