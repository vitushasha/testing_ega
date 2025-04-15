from rest_framework import serializers
from django.contrib.auth import authenticate

class CustomAuthTokenSerializer(serializers.Serializer):
    login = serializers.CharField(label="Login")
    password = serializers.CharField(label="Password", style={'input_type': 'password'}, trim_whitespace=False)

    def validate(self, attrs):
        login = attrs.get('login')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), login=login, password=password)
        if not user:
            raise serializers.ValidationError("Неверный логин или пароль")

        attrs['user'] = user
        return attrs