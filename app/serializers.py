from rest_framework import serializers

from app import models


class WeekSerializer(serializers.ModelSerializer):
    is_passed = serializers.SerializerMethodField()

    def get_is_passed(self, obj):
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            return request.user.weeks.filter(week_id=obj.pk).exists()
        return False

    class Meta:
        model = models.Week
        fields = "__all__"


class TrainingSerializer(serializers.ModelSerializer):
    workout_duration = serializers.ReadOnlyField()
    clear_duration = serializers.ReadOnlyField()
    is_passed = serializers.SerializerMethodField()

    def get_is_passed(self, obj):
        request = self.context.get("request")
        if hasattr(request, "user") and request.user.is_authenticated:
            return request.user.trainings.filter(training_id=obj.pk).exists()
        return False

    class Meta:
        model = models.Training
        fields = "__all__"


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExerciseType
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):
    exercise_type = ExerciseTypeSerializer(read_only=True)

    class Meta:
        model = models.Exercise
        fields = "__all__"
