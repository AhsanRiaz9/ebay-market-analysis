from django.contrib import admin
from django.urls import path, include
# from rest_framework import permissions
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

from role_management.views import (
    
    UserAPIView, UserObjectView,
    ModuleAPIView, ModuleView, ModuleObjectView,
    RoleAPIView , RoleObjectView,
    PermissionAPIView, PermissionObjectView,
    CustomTokenObtainPairView, TokenInfoView, CheckTokenPermissions
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
    TokenVerifyView,
)


# schema_view = get_schema_view(
#    openapi.Info(
#       title="role_management",
#       default_version='v1',
#       description="API documentation",
#     #   terms_of_service="https://www.role_management.com/terms/",
#     #   contact=openapi.Contact(email="contact@role_management.com"),
#     #   license=openapi.License(name="Your License"),
#    ),
#    public=True,
#    permission_classes=(permissions.AllowAny,),
# )

urlpatterns = [
    
    # path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    # path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/token/info/', TokenInfoView.as_view(), name='token-info'),
    path('api/token/validate/', CheckTokenPermissions.as_view(), name='token-validation'),


    #User Handling
    path("users/", UserAPIView.as_view(), name="users-list"),     
    path("users/<int:user_id>/", UserObjectView.as_view(), name="get-user"),
 
    #Permissison Handling
    path("permissions/", PermissionAPIView.as_view(), name="permission-list-create"),
    path("permissions/<int:permission_id>/", PermissionObjectView.as_view(), name="get-permissions"),

    #Roles Handling
    path("roles/", RoleAPIView.as_view(), name="role-list-create"),
    path("roles/<int:role_id>/", RoleObjectView.as_view(), name = "user-role" ), 
    
    #Module Handling
    path("modules/", ModuleAPIView.as_view(), name="module-list"),
    path("get-modules-permissions/", ModuleView.as_view(), name="module-list"),
    path("modules/<int:module_id>/", ModuleObjectView.as_view()),
    
]
