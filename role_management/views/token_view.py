from rest_framework_simplejwt.views import TokenObtainPairView
from role_management.serializers import CustomTokenObtainPairSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from role_management.utils import check_token_expiry, decode_jwt, check_permissions

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    

class TokenInfoView(APIView):
    def get(self, request):
        token = request.META.get('HTTP_AUTHORIZATION').split(' ')[1]  # Assuming Bearer token
        expiry_info = check_token_expiry(token)
        return Response({"message": expiry_info})


class CheckTokenPermissions(APIView):
    def post(self, request, *args, **kwargs):
        token = request.data.get('token')
        if not token:
            return Response({'detail': 'Token not provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        decoded_token = decode_jwt(token)
        # print(decoded_token)
        if not decoded_token:
            return Response({'detail': 'Invalid  token'}, status=status.HTTP_401_UNAUTHORIZED)
        
        if not check_permissions(decoded_token):
            # Invalidate the token by not returning it or by another means (e.g., blacklisting)
            return Response({'detail': 'Permissions have been updated, token expired'}, status=status.HTTP_401_UNAUTHORIZED)
        
        return Response({'detail': 'Token is valid'}, status=status.HTTP_200_OK)
