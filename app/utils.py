from django.db.models import Sum


def update_duration(training, do_update=True):
    warm_up = 300 if training.has_warm_up else 0
    cool_down = 300 if training.has_cool_down else 0
    duration_value = training.exercises.aggregate(duration=Sum("duration")).get("duration", 0) or 0
    print(training)
    result = sum((warm_up, cool_down, duration_value * training.repetitions_number))
    if do_update:
        from app.models import Training
        Training.objects.filter(pk=training.pk).update(duration=result)
        return True
    return result
