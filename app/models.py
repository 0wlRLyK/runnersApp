from django.db import models
from django.utils.html import mark_safe
from file_field_utils.db.fields import SVGAndImageField
from ordered_model.models import OrderedModel

from app.utils import update_duration


class Week(OrderedModel):
    title = models.CharField(max_length=128)
    image = SVGAndImageField(blank=True, upload_to="weeks/")

    def __str__(self):
        return self.title

    @property
    def last_training(self):
        return self.trainings.last()

    def admin_image(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' height='120' />")

    admin_image.short_description = 'Image'
    admin_image.allow_tags = True

    class Meta:
        ordering = ("order",)


class Training(OrderedModel):
    week = models.ForeignKey("app.Week", on_delete=models.CASCADE, related_name="trainings")
    title = models.CharField(max_length=128)
    image = SVGAndImageField(blank=True, upload_to="trainings/")
    duration = models.PositiveIntegerField(default=0, help_text="Training duration in seconds")
    repetitions_number = models.PositiveSmallIntegerField(default=1)
    has_warm_up = models.BooleanField(default=True)
    has_cool_down = models.BooleanField(default=True)
    order_with_respect_to = "week"

    @property
    def is_last_training(self):
        return self.week.last_training.pk == self.pk

    def save(self, *args, **kwargs):
        self.duration = update_duration(self, do_update=False)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order} - {self.title}"

    def admin_image(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' height='120' />")

    def workout_duration(self):
        minutes, seconds = divmod(self.duration % 3600, 60)
        return f"{minutes} minutes"

    def clear_duration(self):
        warm_up = 300 if self.has_warm_up else 0
        cool_down = 300 if self.has_cool_down else 0
        return self.duration - warm_up - cool_down

    admin_image.short_description = 'Image'
    admin_image.allow_tags = True
    workout_duration.short_description = 'Workout duration'
    workout_duration.allow_tags = True
    clear_duration.short_description = 'Clear duration'
    clear_duration.allow_tags = True

    class Meta:
        ordering = ("week", "order")


class Exercise(OrderedModel):
    training = models.ForeignKey("app.Training", on_delete=models.CASCADE, related_name="exercises")
    exercise_type = models.ForeignKey("app.ExerciseType", on_delete=models.CASCADE, related_name="items")
    duration = models.PositiveIntegerField(default=0, help_text="Exercise duration in seconds")
    order_with_respect_to = "training"

    def __str__(self):
        return f"{self.training} - {self.exercise_type}: {self.duration}"

    class Meta:
        ordering = ("training", "order")


class ExerciseType(models.Model):
    title = models.CharField(max_length=128)
    description = models.TextField(default="", blank=True)
    tips = models.TextField(default="", blank=True)
    image = SVGAndImageField(blank=True, upload_to="exercises/")

    def __str__(self):
        return self.title

    def admin_image(self):
        if self.image:
            return mark_safe(f"<img src='{self.image.url}' height='120' />")

    admin_image.short_description = 'Image'
    admin_image.allow_tags = True
