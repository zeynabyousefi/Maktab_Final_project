from django.db import models
from users.models import CustomUser
import os


# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.username, filename)


class Email(models.Model):
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_created=True)
    author_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    attachment = models.FileField(upload_to=user_directory_path, null=True, blank=True)


class EmailPlaceHolders(models.Model):
    place_holder = models.CharField(max_length=255)


class UserEmailMapped(models.Model):
    email_id = models.ForeignKey(Email, on_delete=models.DO_NOTHING)
    user_id = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    place_holder_id = models.ForeignKey(EmailPlaceHolders, on_delete=models.DO_NOTHING)
    is_read = models.BooleanField()
    is_starred = models.BooleanField()


