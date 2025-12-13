from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Customers


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )

        # создаём связанный объект Customers
        Customers.objects.create(
            user=user,
            first_name=user.first_name,
            last_name=user.last_name,
            age=0
        )

        # аккаунт пока неактивен до подтверждения почты
        user.is_active = False
        user.save()
        return user
