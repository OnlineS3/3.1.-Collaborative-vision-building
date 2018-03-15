from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Channel(models.Model):
    room_id = models.CharField(max_length=64)
    channel_name = models.CharField(max_length=128)
    rc_channel = models.CharField(max_length=256)

class VisionSession(models.Model):
    user_email = models.CharField(max_length=128)
    session_name = models.CharField(max_length=128)
    session_description = models.CharField(max_length=512)
    phase = models.IntegerField()
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    region = models.CharField(max_length=128)
    share_id = models.CharField(max_length=40)
    private = models.BooleanField(default=False)

    class Meta:
        app_label = 'cvbapp'

class VisionStatement(models.Model):
    session = models.ForeignKey(VisionSession, on_delete=models.CASCADE)
    user_email = models.CharField(max_length=128)
    vision_statement = models.CharField(max_length=512)
    phase = models.IntegerField()

    class Meta:
        app_label = 'cvbapp'

class VisionReport(models.Model):
    session = models.ForeignKey(VisionSession, on_delete=models.CASCADE)
    vision_report = models.CharField(max_length=1024)

    class Meta:
        app_label = 'cvbapp'

class ScheduledMeeting(models.Model):
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE)
    datetime = models.CharField(max_length=16)
    phase = models.IntegerField()

    class Meta:
        app_label = 'cvbapp'

class Shares(models.Model):
    session = models.ForeignKey(VisionSession, on_delete=models.CASCADE)
    shared_with = models.CharField(max_length=100)

    class Meta:
        app_label = 'cvbapp'