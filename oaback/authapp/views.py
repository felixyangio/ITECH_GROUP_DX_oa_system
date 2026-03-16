from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import LoginSerializer, ResetPwdSerializer, UserInfoSerializer


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        user = authenticate(request, username=email, password=password)
        if not user:
            return Response({'detail': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_active:
            return Response({'detail': 'Account is disabled'}, status=status.HTTP_400_BAD_REQUEST)
        refresh = RefreshToken.for_user(user)
        return Response({
            'token': str(refresh.access_token),
            'refresh': str(refresh),
            'user': UserInfoSerializer(user).data,
        })


class ResetPwdView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ResetPwdSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        if not user.check_password(serializer.validated_data['oldpwd']):
            return Response({'detail': 'Incorrect old password'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(serializer.validated_data['pwd1'])
        user.save()
        return Response({'detail': 'Password changed successfully'})
