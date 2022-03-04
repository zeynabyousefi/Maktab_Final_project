# Generated by Django 4.0.2 on 2022-03-02 08:33

from django.db import migrations, models
import emails.validators


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0011_alter_email_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='<function user_directory_path at 0x7efed88df6d0>/', validators=[emails.validators.validate_file_size]),
        ),
    ]