from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
import ticket.DBOPS.MongoDBOps as db
from .forms import FormNewTicket
import datetime


@login_required(login_url="/account/login/")
def view_tickets_list(request):
    tickets = db.getTickets(request.user)
    context = {
        'tickets': tickets,
        "trouble_page": "active"
    }
    return render(request, "tickets.html", context)


@login_required(login_url="/account/login/")
def view_create_tickets(request):
    if request.method == 'POST':
        form = FormNewTicket(data = request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            ticket_name = form.cleaned_data['ticket_name']
            assignment_name = form.cleaned_data['assignment_name']
            author = form.cleaned_data['author']
            timestamp = datetime.datetime.now()
            comments = form.cleaned_data['comments']
            db.insertTicket(ticket_id, ticket_name, assignment_name, author, timestamp, comments)
            return redirect("ticket:view_tickets_list")
    else:
        form = FormNewTicket()
    assignments = db.getMyAssignments(str(request.user))
    cnt = db.getLastTickCnt(str(request.user))
    tid = str(datetime.datetime.now().strftime('%m%d%Y%H%M%S'))
    context = {
        "form": form,
        "mytimestamp": datetime.datetime.now(),
        "assignments": assignments,
        'tid': tid + "_TT" + str(cnt),
    }
    return render(request, "create_ticket.html", context)


@login_required(login_url="/account/login/")
def view_delete_tickets(request, tid):
    db.deleteTicket(str(tid))
    return redirect("ticket:view_tickets_list")


@login_required(login_url="/account/login/")
def view_change_ticket_status(request, tid):
    db.changeTicketStatus(str(tid))
    return redirect("ticket:view_tickets_list")


@login_required(login_url="/account/login/")
def view_associate_tickets(request, assign):
    if request.method == 'POST':
        form = FormNewTicket(data = request.POST)
        if form.is_valid():
            ticket_id = form.cleaned_data['ticket_id']
            ticket_name = form.cleaned_data['ticket_name']
            assignment_name = form.cleaned_data['assignment_name']
            print("ASSIGNMENT NAME :: ", assignment_name)
            author = form.cleaned_data['author']
            timestamp = datetime.datetime.now()
            comments = form.cleaned_data['comments']
            db.insertTicket(ticket_id, ticket_name, assignment_name, author, timestamp, comments)
            return redirect("ticket:view_tickets_list")
    else:
        form = FormNewTicket()

    cnt = db.getLastTickCnt(str(request.user))
    tid = str(datetime.datetime.now().strftime('%m%d%Y+%H%M%S'))
    context = {
        "form": form,
        "mytimestamp": datetime.datetime.now(),
        "assignment_name": assign,
        'tid': tid + "_TT" + str(cnt),
    }
    return render(request, "associate_ticket.html", context)