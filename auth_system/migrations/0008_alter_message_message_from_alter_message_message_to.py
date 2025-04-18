# Generated by Django 5.2 on 2025-04-17 11:50

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth_system', '0007_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='message_from',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_from', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='message',
            name='message_to',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_to', to=settings.AUTH_USER_MODEL),
        ),
    ]
