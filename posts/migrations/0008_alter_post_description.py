# Generated by Django 5.1.6 on 2025-04-15 07:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_remove_post_likes_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, max_length=445, null=True),
        ),
    ]
