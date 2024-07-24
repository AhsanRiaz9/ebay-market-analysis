from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from collections import defaultdict


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] =user.name
        token["email"] = user.email
        token["role"] = user.role.name

        module_permissions = defaultdict(list)

        # Group permissions by module
        for permission in user.role.permissions.all():
            module_permissions[permission.module.name].append(
                {
                    "name": permission.name,
                    "code": permission.code,
                    "module_id": permission.module.id,
                }
            )

        # Convert defaultdict to a regular dict and add to token
        token["permissions"] = dict(module_permissions)

        return token
