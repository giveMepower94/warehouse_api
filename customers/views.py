from rest_framework import generics
from django.contrib.auth.models import User
from .serializers import UserRegistrationSerializer
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from .models import EmailVerificationToken


# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer


class VerifyEmailView(GenericAPIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request, token):
        token_obj = get_object_or_404(EmailVerificationToken, token=token)

        if token_obj.is_expired():
            return Response(
                {"detail": "Token expired"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = token_obj.user
        user.is_active = True
        user.save(update_fields=['is_active'])

        token_obj.delete()

        return Response({"detail": "Email verified successfully"})
