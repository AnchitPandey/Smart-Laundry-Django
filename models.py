# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class student(models.Model):
    name = models.CharField(max_length=40)
    password = models.CharField(max_length=50)
    bits_id = models.CharField(max_length=13,primary_key=True)
    gender = models.CharField(max_length=10)
    email_id = models.CharField(max_length = 50,null =True)
    usertype =  models.CharField(max_length = 50, default="student")
    current_count = models.IntegerField(default =0)
    max_count = models.IntegerField(default = 40)
    inactive_status = models.CharField(max_length =  50, default= "inactive")
    
    def __str__(self):
        return self.name

class data(models.Model):
    #idd = models.ForeignKey('student')
    idd = models.CharField(max_length = 13)
    month = models.CharField(max_length = 20,null=True)
    count=  models.IntegerField(null=True)
    time_stamp = models.DateTimeField(null=True)
    cost = models.DecimalField(decimal_places=2,max_digits=5, default =0)
    machine_number = models.IntegerField(null=True)
    machine_state = models.NullBooleanField(null=True)
    last_used = models.DateTimeField(null=True)
    

    def __str__(self):
        return self.idd


class Admin(models.Model):
    username = models.CharField(max_length = 30)
    password = models.CharField(max_length = 20)
    def __str__(self):
        return self.username
        




