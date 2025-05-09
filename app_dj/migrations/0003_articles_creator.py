# Generated by Django 5.1.7 on 2025-04-12 18:27

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("app_dj", "0002_create_superuser"),
    ]

    operations = [
        migrations.AddField(
            model_name="articles",
            name="creator",
            field=models.ForeignKey(
                default=1,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="articles",
                to=settings.AUTH_USER_MODEL,
            ),
            preserve_default=False,
        ),
    ]
