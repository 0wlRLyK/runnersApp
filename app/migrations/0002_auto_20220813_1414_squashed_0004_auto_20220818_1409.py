# Generated by Django 3.2.15 on 2022-08-18 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    replaces = [('app', '0002_auto_20220813_1414'), ('app', '0003_auto_20220813_1418'), ('app', '0004_auto_20220818_1409')]

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='week',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='week',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ('order',)},
        ),
        migrations.AddField(
            model_name='exercise',
            name='order',
            field=models.PositiveIntegerField(db_index=True, default=0, editable=False, verbose_name='order'),
            preserve_default=False,
        ),
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ('training', 'order')},
        ),
        migrations.AddField(
            model_name='training',
            name='has_cool_down',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='training',
            name='has_warm_up',
            field=models.BooleanField(default=True),
        ),
    ]