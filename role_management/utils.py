from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import AccessToken
from datetime import datetime
import jwt
import base64
import json
from django.conf import settings
from role_management.models import CustomUser, Role, Permission


def check_token_expiry(token):
    try:
        decoded_token = AccessToken(token)
        expiry_timestamp = decoded_token.payload["exp"]

        if datetime.utcnow() > datetime.utcfromtimestamp(expiry_timestamp):
            return "Token has expired."
        else:
            return f"Token expires at: {datetime.fromtimestamp(expiry_timestamp)}"
    except TokenError as e:
        return f"Token decode error: {str(e)}"


def decode_jwt(token):
    try:
        
        # Split the token into parts and ensure there are three parts
        token_parts = token.split('.')
        if len(token_parts) != 3:
            raise jwt.InvalidTokenError("Invalid token format")
        
        decoded_payload = base64.urlsafe_b64decode(token_parts[1] + '==').decode('utf-8')
        
        decoded_token=json.loads(decoded_payload)
        return decoded_token
    
    except jwt.ExpiredSignatureError:
        print("Signature has expired")
        return None
    
    except jwt.InvalidTokenError as e:
        print("Invalid Token:", str(e))
        return None

def check_permissions(decoded_token):
    if not decoded_token:
        print("Token is None")
        return False

    user_id = decoded_token.get("user_id")
    token_roles = decoded_token.get("role")
    token_permissions = decoded_token.get("permissions")

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        print(f"User with id {user_id} does not exist")
        return False

    user_roles = Role.objects.filter(customuser=user)
    user_permissions = Permission.objects.filter(role__in=user_roles).distinct()
    # print(user_roles, user_permissions)
    current_roles = [role.name for role in user_roles]
    current_permissions = [permission.name for permission in user_permissions]
    # print(current_roles, current_permissions)
    if set(token_roles) != set(current_roles) or set(token_permissions) != set(current_permissions):
        print("token_permissions", set(token_permissions))
        print("token_roles", set(token_roles))
        print("current_permissions", set(current_permissions))
        print("current_roles", set(token_roles))
        print("Roles or permissions do not match")
        return False

    return True

