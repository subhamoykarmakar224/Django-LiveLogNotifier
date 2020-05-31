from django.db import models
import datetime


class Ticket(models.Model):
    ticket_id = models.CharField(max_length=50)
    ticket_name = models.CharField(max_length=100)
    assignment_name = models.CharField(max_length=120)
    author = models.CharField(max_length=120)
    createdon = models.CharField(max_length=100)
    comments = models.TextField(blank=True, )
