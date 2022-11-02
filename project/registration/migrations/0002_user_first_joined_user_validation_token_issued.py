# Generated by Django 4.1.3 on 2022-11-01 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("registration", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="first_joined",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="user",
            name="validation_token_issued",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]