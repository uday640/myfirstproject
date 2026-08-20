from django.db import models
from django.contrib.auth.models import User

class key_storage(models.Model):
    aes_key=models.BinaryField()
    hashcode=models.CharField(max_length=64)
    auther=models.ForeignKey(User,on_delete=models.CASCADE,default=None)
    files=models.BinaryField(null=True,blank=True)
    name=models.CharField(max_length=255)