# Generated by Django 4.0.1 on 2022-02-23 18:21

from django.db import migrations, models
import emails.models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to=emails.models.user_directory_path),
        ),
    ]