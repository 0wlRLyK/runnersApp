# Generated by Django 3.2.15 on 2022-08-18 18:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20220813_1414_squashed_0004_auto_20220818_1409'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PassedWeek',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='weeks', to=settings.AUTH_USER_MODEL)),
                ('week', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.week')),
            ],
        ),
        migrations.CreateModel(
            name='PassedTraining',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.training')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='trainings', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddConstraint(
            model_name='passedweek',
            constraint=models.UniqueConstraint(fields=('user', 'week'), name='unique_user_week'),
        ),
        migrations.AddConstraint(
            model_name='passedtraining',
            constraint=models.UniqueConstraint(fields=('user', 'training'), name='unique_user_training'),
        ),
    ]
