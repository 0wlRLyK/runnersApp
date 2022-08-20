from authemail.models import SignupCode, send_multi_format_email
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from app.models import Training

from . import models

User = get_user_model()


class TokenSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        try:
            token['avatar'] = user.profile.avatar.url if user.profile.avatar else ""
        except models.Profile.DoesNotExist:
            token['avatar'] = ""

        return token


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(validators=[UniqueValidator(queryset=User.objects.all())])
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        must_validate_email = getattr(settings, "AUTH_EMAIL_VERIFICATION", True)
        validated_data.pop("password2")
        user = User.objects.create(
            username=validated_data.pop('username'),
            email=validated_data.pop('email'),
            is_verified=not must_validate_email,
            **validated_data
        )
        if not must_validate_email:
            send_multi_format_email('welcome_email',
                                    {'email': user.email, },
                                    target_email=user.email)

        user.set_password(validated_data['password'])
        user.save()

        if must_validate_email:
            # Create and associate signup code
            request = self.context['request']
            ipaddr = request.META.get('REMOTE_ADDR', '0.0.0.0')
            signup_code = SignupCode.objects.create_signup_code(user, ipaddr)
            signup_code.send_signup_email()
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Profile
        exclude = ["user", "id"]


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = User
        exclude = ["password", "last_login", "is_superuser", "is_staff", "is_active", "groups", "user_permissions"]
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "username": {"read_only": True}
        }

    def update(self, instance, validated_data):
        if "profile" in validated_data:
            profile = ProfileSerializer(instance=instance.profile, data=validated_data.pop("profile"), partial=True)
            profile.is_valid(raise_exception=True)
            profile.save()
        return super().update(instance, validated_data)


class PassedActivitySerializer(serializers.Serializer):
    training = serializers.PrimaryKeyRelatedField(queryset=Training.objects.all())
