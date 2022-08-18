from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from app.models import Exercise
from app.utils import update_duration


@receiver([post_save, pre_delete], sender=Exercise)
def update_duration_signal(instance, **kwargs):
    update_duration(instance.training, do_update=True)
