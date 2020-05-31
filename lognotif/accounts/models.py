from django.db import models


class NewUser(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    role = models.CharField(max_length=100)


class ModelNewServer(models.Model):
    servername = models.CharField(max_length=100)
    loglocation = models.CharField(max_length=100)
    createdby = models.CharField(max_length=100)
