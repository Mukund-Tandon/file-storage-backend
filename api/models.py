from django.db import models
from uuid import uuid4
import uuid
from statistics import mode
import os
from channels.layers import get_channel_layer
from asgiref.sync import  async_to_sync
import json
# Create your models here.


class User(models.Model):
    uid = models.CharField(primary_key=True ,max_length=100)
    email = models.EmailField(unique=True)
    premium = models.BooleanField(default=False)
    used_space = models.DecimalField(max_digits=10,decimal_places=3,default=0.0)

    def __str__(self):
        return self.email
class Folder(models.Model):
    uid = models.UUIDField(primary_key=True,editable=False, default=uuid.uuid4)
    created_at = models.DateTimeField(auto_now=True)

def get_upload_path(instance, filename):
    return os.path.join(str(instance.uploaded_by), filename)

class File(models.Model):
    uploaded_by = models.EmailField()
    file = models.FileField(upload_to=get_upload_path)
    created_at = models.DateTimeField(auto_now=True)

class StripeSubscriber(models.Model):
    user = models.OneToOneField(to=User, on_delete=models.CASCADE,default=None)
    stripeCustomerId = models.CharField(max_length=255)
    stripeSubscriptionId = models.CharField(max_length=255)
    start_time = models.CharField(max_length=255,default='0')
    end_time = models.CharField(max_length=255,default='0')
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        channel_layer=get_channel_layer()
        data={'status':'completed'}
        async_to_sync(channel_layer.group_send)(
            'test_group',{
                'type':'send_task_completed_signal',
                'value':data
            }
        )
        super(StripeSubscriber,self).save()


    def __str__(self):
        return self.user.email
