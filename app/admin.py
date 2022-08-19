from django.contrib import admin
from ordered_model.admin import OrderedModelAdmin

from app.models import Exercise, ExerciseType, Training, Week


class TrainingInline(admin.StackedInline):
    model = Training


class ExerciseInline(admin.StackedInline):
    model = Exercise


@admin.register(Week)
class WeekAdmin(OrderedModelAdmin):
    inlines = (TrainingInline,)
    list_display = ("title", 'admin_image', 'move_up_down_links')
    readonly_fields = ('admin_image',)


@admin.register(Training)
class TrainingAdmin(OrderedModelAdmin):
    inlines = (ExerciseInline,)
    list_display = ("title", 'admin_image', 'move_up_down_links')
    readonly_fields = ('admin_image', 'workout_duration', 'clear_duration')


@admin.register(Exercise)
class ExerciseAdmin(OrderedModelAdmin):
    list_display = ("training", "exercise_type", "duration", 'move_up_down_links')
    list_filter = ("training", "exercise_type",)


@admin.register(ExerciseType)
class ExerciseTypeAdmin(admin.ModelAdmin):
    list_display = ("title", 'admin_image',)
    readonly_fields = ('admin_image',)
