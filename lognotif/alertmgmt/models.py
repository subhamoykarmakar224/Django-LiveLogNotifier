from django.db import models


class LogFile(models.Model):
    comments = models.TextField(null=True, blank=True)


class LogFilterFields(models.Model):
    severity_sort = models.CharField(max_length=128)
    timestamp_sort = models.CharField(max_length=128)
    start_date = models.CharField(max_length=128)
    start_time = models.CharField(max_length=128, default='00:00:00', null=False)
    end_date = models.CharField(max_length=128)
    end_time = models.CharField(max_length=128, default='23:59:59', null=False)
    page_no = models.IntegerField(default=1)
    log_src_url = models.CharField(max_length=100, default="all")


class NewAssignment(models.Model):
    assignment_name = models.CharField(max_length=128)
    assignee = models.CharField(max_length=100)
    assignto = models.CharField(max_length=100)
    ackstatus = models.BooleanField(default=False, blank=False, null=False)
    loglist = models.TextField(blank=False, null=False, default="ALL")
