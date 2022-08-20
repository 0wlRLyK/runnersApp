from django.contrib.auth import get_user_model
from django.db import IntegrityError
from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from . import models, serializers

User = get_user_model()


class NewTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.TokenSerializer


class RegisterUserAPIView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = models.User.objects.all()
    serializer_class = serializers.RegisterSerializer

    def post(self, request, *args, **kwargs):
        result = self.create(request, *args, **kwargs)
        try:
            user = get_user_model().objects.get(email=result.data.get("email"))
        except get_user_model().DoesNotExist:
            user = request.user
        refresh = serializers.TokenSerializer.get_token(user)
        access = refresh.access_token
        data = {
            "refresh": refresh.__str__(),
            "access": access.__str__()
        }
        result.data.update(data)
        return result


class RetrieveUpdateCurrentUserAPIView(generics.RetrieveUpdateAPIView):
    queryset = models.User.objects.all()
    serializer_class = serializers.UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(self.get_queryset(), **{"pk": self.request.user.pk})


class UpdateUserActivityAPIView(generics.GenericAPIView):
    queryset = models.PassedTraining.objects.all()
    serializer_class = serializers.PassedActivitySerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        training = serializer.validated_data.get("training")
        try:
            models.PassedTraining.objects.create(training=training, user=request.user)
        except IntegrityError:
            raise ValidationError({"training": "This training is already passed"})
        message = f"Training {training} of {training.week} passed successfully!"
        if training.is_last_training:
            week = models.PassedWeek.objects.create(week=training.week, user=request.user)
            message = f"Training {training} and week {week.week} of passed successfully!"
        return Response({
            "result": message
        })
