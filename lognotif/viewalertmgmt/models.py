from django.db import models


class ReAssignment(models.Model):
    assignment_name = models.CharField(max_length=128)
    assignee = models.CharField(max_length=100)
    assignto = models.CharField(max_length=100)
