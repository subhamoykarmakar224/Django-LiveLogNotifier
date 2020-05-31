from django.shortcuts import render, redirect
import viewalertmgmt.DBOPS.MongoDBOps as db
from django.contrib.auth.decorators import login_required
from .form import FormReAssignment
from django.contrib.auth.models import User


@login_required(login_url="/account/login/")
def alert_mgnt_dash(request):
    user = request.user
    assignedToMe = db.getMyAssignments(str(user))
    assignee = db.getAssignmentTo(str(user))
    userlist = User.objects.all()
    context = {
        'alert_mng_page': 'active',
        'assignedToMe': assignedToMe,
        'assignee': assignee,
        "selected": '',
        'userlist': userlist,

    }
    return render(request, "alertdash.html", context)


@login_required(login_url="/account/login/")
def ack_alert_view(request, alert_name):
    if request.method == 'POST':
        db.changeAckFlag(alert_name)

    return redirect("viewalertmgmt:alert_mgnt_dash")


@login_required(login_url="/account/login/")
def ack_alert_log_view(request, alert_name):
    if request.method == 'POST':
        user = request.user
        assignedToMe = db.getMyAssignments(str(user))
        assignee = db.getAssignmentTo(str(user))
        logdata = db.getLogData(alert_name)
        userlist = User.objects.all()
        context = {
            'alert_mng_page': 'active',
            'assignedToMe': assignedToMe,
            'assignee': assignee,
            "logdata": logdata,
            "selected": alert_name,
            'userlist': userlist
        }
        return render(request, "alertdash.html", context)

    # user = request.user
    # assignedToMe = db.getMyAssignments(str(user))
    # assignee = db.getAssignmentTo(str(user))
    # logdata = db.getLogData(alert_name)
    # userlist = User.objects.all()
    # context = {
    #     'alert_mng_page': 'active',
    #     'assignedToMe': assignedToMe,
    #     'assignee': assignee,
    #     "logdata": logdata,
    #     "selected": alert_name,
    #     "reassign_form": FormReAssignment(),
    #     'userlist': userlist
    # }
    return redirect('viewalertmgmt:alert_mgnt_dash')


@login_required(login_url="/account/login/")
def ack_alert_delete(request, alert_name):
    if request.method == 'POST':
        db.delCompleteAssignment(alert_name)

    return redirect('viewalertmgmt:alert_mgnt_dash')


@login_required(login_url="/account/login/")
def alert_reassign_view(request, alert_name):
    form = FormReAssignment(request.POST or None)
    if request.method == "POST" and form.is_valid():
        assignment_name = (form.cleaned_data['assignment_name'])
        assignee = (form.cleaned_data['assignee'])
        assignto = (form.cleaned_data['assignto'])
        db.updateCompleteAssignment(
            assignment_name, assignee, assignto
        )
        return redirect("viewalertmgmt:alert_mgnt_dash")

    assignedTo = db.getAssignedToName(alert_name)
    userlist = User.objects.all()
    context = {
        "form": form,
        "alert_name": alert_name,
        "userlist": userlist,
        "assignedTo": str(assignedTo).strip(" ")
    }
    return render(request, "reassign.html", context)

