from rest_framework import serializers

from app import models


class WeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Week
        fields = "__all__"


class TrainingSerializer(serializers.ModelSerializer):
    workout_duration = serializers.ReadOnlyField()
    clear_duration = serializers.ReadOnlyField()

    class Meta:
        model = models.Training
        fields = "__all__"


class ExerciseTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ExerciseType
        fields = "__all__"


class ExerciseSerializer(serializers.ModelSerializer):
    exercise_type = ExerciseTypeSerializer()

    class Meta:
        model = models.Exercise
        fields = "__all__"
