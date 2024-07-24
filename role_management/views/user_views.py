from rest_framework import status, generics
from django.contrib.auth import login
from role_management.models import CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from role_management.paginator import CustomPagination
from role_management.serializers import (
    CustomUserSerializer,
    CustomRegisterSerializer,
)
from django.shortcuts import get_object_or_404
from role_management.permissions import HasPermission
from rest_framework.permissions import IsAuthenticated


class UserAPIView(APIView):

    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_user"
        elif self.request.method == "POST":
            required_permission_code = "add_user"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]
    pagination_class = CustomPagination

    def get(self, request):
        user = CustomUser.objects.all()
        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(user, request)
        total_pages = paginator.page.paginator.num_pages

        serializers = CustomUserSerializer(paginated_users, many=True)
        return paginator.get_paginated_response(serializers.data)

    def post(self, request):
        data = {
            key: value.lower() if isinstance(value, str) else value
            for key, value in request.data.items()
        }

        serializers = CustomRegisterSerializer(data=data)
        if serializers.is_valid():
            serializers.save()
            return Response(
                data={
                    "message": "User Created Successfully",
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class UserObjectView(APIView):
    def allowed_permission(self):
        if self.request.method == "GET":
            required_permission_code = "view_user"
        elif self.request.method == "PUT":
            required_permission_code = "update_user"
        elif self.request.method == "DELETE":
            required_permission_code = "delete_user"
        return required_permission_code

    permission_classes = [IsAuthenticated, HasPermission]

    def get(self, request, user_id):

        user = get_object_or_404(CustomUser, id=user_id)
        serializers = CustomRegisterSerializer(user)
        return Response(serializers.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):

        user = get_object_or_404(CustomUser, id=user_id)
        serializers = CustomRegisterSerializer(user, data=request.data)
        if serializers.is_valid():
            serializers.save()

            return Response(serializers.data, status=status.HTTP_200_OK)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):

        user = get_object_or_404(CustomUser, id=user_id)
        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


# class CustomUserLoginView(APIView):
#     def post(self, request):
#         serializer = CustomLoginSerializer(
#             data=request.data, context={"request": request}
#         )
#         if serializer.is_valid():
#             user = serializer.validated_data.get("user")
#             if user:
#                 login(request, user)
#                 return Response(
#                     {"message": "User Logged in Successfully"},
#                     status=status.HTTP_200_OK,
#                 )
#             else:
#                 return Response(
#                     {"message": "Authentication failed"},
#                     status=status.HTTP_401_UNAUTHORIZED,
#                 )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CustomAuthToken(APIView):
#     def post(self, request):
#         email = request.data.get('email')
#         password = request.data.get('password')
#         try:
#             user = CustomUser.objects.get(email=email)
#         except CustomUser.DoesNotExist:
#             return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)

#         user = authenticate(username=user.email, password=password)
#         if user is not None:
#             token, created = Token.objects.get_or_create(user=user)
#             return Response({"token": token.key})
#         return Response({"error": "Invalid email or password"}, status=status.HTTP_400_BAD_REQUEST)
