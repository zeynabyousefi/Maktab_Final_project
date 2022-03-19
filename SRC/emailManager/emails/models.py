from django.db import models
from users.models import CustomUser
import os
from .validators import *


# Create your models here.


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT / user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.author.username, filename)


class Email(models.Model):
    subject = models.CharField(max_length=200, blank=True, null=True)
    body = models.TextField(null=True, blank=True)
    created_date = models.DateTimeField(auto_created=True, auto_now_add=True)
    author = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING)
    attachment = models.FileField(upload_to=user_directory_path, null=True, blank=True,
                                  validators=[validate_file_size])
    reply = models.ForeignKey('self', null=True, blank=True, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f'author: {self.author.username} subject: {self.subject}'


class EmailReceiver(models.Model):
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
    to = models.ManyToManyField(CustomUser, blank=True, related_name='to')
    cc = models.ManyToManyField(CustomUser, blank=True, related_name='cc')
    bcc = models.ManyToManyField(CustomUser, blank=True, related_name='bcc')

    def __str__(self):
        to_string = ", ".join(str(to) for to in self.to.all())
        cc_string = ", ".join(str(cc) for cc in self.cc.all())
        bcc_string = ", ".join(str(bcc) for bcc in self.bcc.all())

        return f'to: {to_string}; cc: {cc_string}; bcc:{bcc_string}'


class EmailPlaceHolders(models.Model):
    place_holder = models.CharField(max_length=255,unique=True)
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return f'{self.place_holder}'


class UserEmailMapped(models.Model):
    email = models.ForeignKey(Email, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, blank=True, null=True)
    place_holder = models.ForeignKey(EmailPlaceHolders, on_delete=models.DO_NOTHING)
    is_read = models.BooleanField(default=False)
    is_starred = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user}'

