from django.db import models
from uuid import uuid4
import uuid
from statistics import mode
import os
# Create your models here.


class User(models.Model):
    uid = models.CharField(max_length=100)
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
