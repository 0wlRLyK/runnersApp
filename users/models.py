from authemail.models import EmailAbstractUser
from django.contrib.auth.models import UserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(EmailAbstractUser):
    username_validator = UnicodeUsernameValidator()
    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[username_validator],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ("email",)

    def __str__(self):
        return self.username


class Profile(models.Model):
    class SexChoices(models.IntegerChoices):
        UNDEFINED = 0
        MALE = 1
        FEMALE = 2

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    avatar = models.ImageField(upload_to="users/avatar/", blank=True)
    sex = models.PositiveSmallIntegerField(choices=SexChoices.choices, default=0)
    birthdate = models.DateField(blank=True, null=True)


class PassedTraining(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="trainings")
    training = models.ForeignKey("app.Training", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'training'], name='unique_user_training')
        ]


class PassedWeek(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="weeks")
    week = models.ForeignKey("app.Week", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'week'], name='unique_user_week')
        ]
