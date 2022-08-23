from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

from accounts.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """Serializer for user creation"""
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=CustomUser.objects.all())]
    )
    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'password', 'password2', 'email',)
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def validate(self, attrs):
        """Check if password1 == password2 repeat"""
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': 'Password fields didn\'t match'}
            )
        return attrs

    def create(self, validated_data):
        """Creating user object if data is valid"""
        user = CustomUser.objects.create(
            email=validated_data['email'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken('No valid token found in cookie \'refresh_token\'')
