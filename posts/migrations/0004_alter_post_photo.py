# Generated by Django 5.1.6 on 2025-04-08 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0003_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
