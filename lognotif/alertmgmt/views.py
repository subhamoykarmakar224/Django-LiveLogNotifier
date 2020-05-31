from django.shortcuts import render, redirect
import datetime
import alertmgmt.configuration as cfg
import alertmgmt.DBOPS.MongoDBOps as dbops
from .forms import FormLogComment, FormLogFilter, FormAssignment
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


@login_required(login_url="/account/login/")
def view_alert(request):
    severity_level_filter = '-1'
    timestamp_filter = -1

    l = dbops.getFirstAndLastData()
    if l['first'] == 0:
        startDate = datetime.date.today()  # 2020-05-03
        startTime = datetime.time.now()  #
        endDate = datetime.date.today()  # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
        endTime = datetime.time.now()  # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
    else:
        startDate = l['first']['datestamp'] # 2020-05-03
        startTime = l['first']['timestamp'] #
        endDate = l['last']['datestamp'] # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S
        endTime = l['last']['timestamp'] # 08:30 PM %I:%M %p => 20:30:23 %H:%M:%S

    startDate = datetime.datetime.strptime(startDate, '%Y-%m-%d').strftime("%B %d, %Y")
    startTime = datetime.datetime.strptime(startTime, '%H:%M:%S').strftime("%I:%M %p")
    endDate = datetime.datetime.strptime(endDate, '%Y-%m-%d').strftime("%B %d, %Y")
    endTime = datetime.datetime.strptime(endTime, '%H:%M:%S').strftime("%I:%M %p")

    pageNo = 1

    res, k, v = getSummaryInfo()

    form = FormLogFilter(request.POST or None)
    if form.is_valid():
        severity_level_filter = form.cleaned_data['severity_sort']
        timestamp_filter = int(form.cleaned_data['timestamp_sort'])
        start_date_filter = (form.cleaned_data['start_date'])
        start_time_filter = (form.cleaned_data['start_time'])
        end_date_filter = (form.cleaned_data['end_date'])
        end_time_filter = (form.cleaned_data['end_time'])
        pageNo = (form.cleaned_data['page_no'])
        log_src_url = (form.cleaned_data['log_src_url'])
        logsource = dbops.getServerURL((form.cleaned_data['log_src_url']))

        date_time_engine = [
            start_date_filter,
            start_time_filter,
            end_date_filter,
            end_time_filter
        ]

        sort_engine = [
            ("log_seq_index", int(timestamp_filter)),
            ("datestamp", int(timestamp_filter)),
            ("timestamp", int(timestamp_filter)),
        ]

        if severity_level_filter != "-1":
            print("CONDITION :: 1")
            logsources = dbops.getUniqueServerLocations()

            logData = dbops.getLogDateAsPerSeverityKey(
                severity_level_filter,
                sort_engine,
                date_time_engine,
                logsource,
                pageNo)

            res, k, v = getSummaryInfoFiltered(severity_level_filter, date_time_engine, logsource)
            userlist = User.objects.all()
            logcount = 0
            for iv in v:
                logcount += int(iv)
            context = {
                "severity_count": res,
                "userlist": userlist,
                "logsources": logsources,
                "logsource": log_src_url,
                "fields": k,
                "values": v,
                "severity_levels": cfg.SEVERITY_LEVELS,
                "view_page": "active",
                "logdata": logData,
                "logcount": logcount,
                "filterform": form,
                "start_date": start_date_filter,
                "end_date": end_date_filter,
                "start_time": start_time_filter,
                "end_time": end_time_filter,
                "severity_level_filter" : severity_level_filter,
                "timestamp_filter": timestamp_filter,
                "page_no": pageNo,
            }
            return render(request, "index.html", context)

        if timestamp_filter != 0:
            print("CONDITION :: 2")
            logsources = dbops.getUniqueServerLocations()

            logData = dbops.getLogDateAsPerTimeStamp(
                sort_engine,
                date_time_engine,
                logsource,
                pageNo)
            res, k, v = getSummaryInfoFiltered(severity_level_filter, date_time_engine, logsource)
            userlist = User.objects.all()
            logcount = 0
            for iv in v:
                logcount += int(iv)
            context = {
                "severity_count": res,
                "userlist": userlist,
                "logsources": logsources,
                "logsource": log_src_url,
                "fields": k,
                "values": v,
                "severity_levels": cfg.SEVERITY_LEVELS,
                "view_page": "active",
                "logdata": logData,
                "logcount": logcount,
                "filterform": form,
                "start_date": start_date_filter,
                "end_date": end_date_filter,
                "start_time": start_time_filter,
                "end_time": end_time_filter,
                "severity_level_filter" : severity_level_filter,
                "timestamp_filter": timestamp_filter,
                "page_no": pageNo,
            }

            return render(request, "index.html", context)
        else:
            return redirect("view_alert")

    form = FormLogFilter()
    form_assign = FormAssignment()
    lastIndex = dbops.getLastLogSeqIndex()
    logData = dbops.getLogDate(lastIndex - 50, lastIndex)
    logsources = dbops.getUniqueServerLocations()
    userlist = User.objects.all()
    logcount = 0
    for iv in v:
        logcount += int(iv)
    context = {
        "severity_count": res,
        "userlist": userlist,
        "logsources": logsources,
        "logsource": 'all',
        "fields": k,
        "values": v,
        "severity_levels": cfg.SEVERITY_LEVELS,
        "view_page": "active",
        "logdata": logData,
        "logcount": logcount,
        "filterform": form,
        "form_assign": form_assign,
        "start_date": startDate,
        "start_time": "12:00 AM",
        "end_date": endDate,
        "end_time": "11:59 PM",
        "severity_level_filter" : severity_level_filter,
        "timestamp_filter": timestamp_filter,
        "page_no": pageNo,
    }
    return render(request, "index.html", context)


@login_required(login_url="/account/login/")
def add_alert_comment(request, log_seq_index):
    logdata = dbops.getSingleLogDate(log_seq_index)
    form = FormLogComment(request.POST or None)
    if form.is_valid():
        dbops.updateLogDataComment(log_seq_index, str(form['comments'].value()).strip())
        return redirect('view_alert')

    context = {
        'log_seq_index': log_seq_index,
        'logdata': logdata[0],
        'form': form
    }
    return render(request, 'add_comment.html', context)


@login_required(login_url="/account/login/")
def view_add_assignment(request):
    if request.method == "POST":
        form = FormAssignment(data=request.POST)
        if form.is_valid():
            dbops.addNewAssignments(
                form.cleaned_data['assignment_name'],
                form.cleaned_data['assignee'],
                form.cleaned_data['ackstatus'],
                form.cleaned_data['loglist'],
                form.cleaned_data['assignto']
            )
            return redirect("view_alert" )

    form = FormAssignment()
    return redirect("view_alert" )


@login_required(login_url="/account/login/")
def view_raw_log(request, src):
    context = {
        "logsource": src
    }
    return render(request, "view_raw.html", context)


def getSummaryInfo():
    res = dbops.getGroupedCount()  # severity_group_count
    k = ['Emergency', 'Alert',  'Critical', 'Error', 'Warning']
    v = []
    colors = []
    for i in k:
        v.append(res[i])

    return res, k, v


def getSummaryInfoFiltered(severity_level_filter, date_time_engine, logsource):
    res = dbops.getGroupedCountFiltered(severity_level_filter, date_time_engine, logsource)  # severity_group_count
    k = ['Emergency', 'Alert',  'Critical', 'Error', 'Warning']
    v = []
    colors = []
    for i in k:
        v.append(res[i])

    return res, k, v
