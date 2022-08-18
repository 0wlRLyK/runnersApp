from django.contrib import admin

from app.models import Exercise, ExerciseType, Training, Week


class TrainingInline(admin.StackedInline):
    model = Training


class ExerciseInline(admin.StackedInline):
    model = Exercise


@admin.register(Week)
class WeekAdmin(admin.ModelAdmin):
    inlines = (TrainingInline,)
    list_display = ("title", 'admin_image',)
    readonly_fields = ('admin_image',)


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    inlines = (ExerciseInline,)
    list_display = ("title", 'admin_image',)
    readonly_fields = ('admin_image', 'workout_duration', 'clear_duration')


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("training", "exercise_type", "duration")
    list_filter = ("training", "exercise_type",)


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ("title", 'admin_image',)
    readonly_fields = ('admin_image',)
