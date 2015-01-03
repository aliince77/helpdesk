# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseRedirect
from django.shortcuts import render_to_response

from helpdesk.models import *
from helpdeskforms import CreateTicketForm
from django.core.urlresolvers import reverse


@login_required
def createTicket(request):
    if request.user.is_authenticated():
        status="Formu doldur"
        initialdata={'status':'1'}
        if request.POST:
            initialdata['department']=Department.objects.get(product=request.POST['product']).pk
            initialdata['createdbyUser']='1'
            initialdata['product']=request.POST['product']
            initialdata['priority']=request.POST['priority']
            initialdata['title']=request.POST['title']
            initialdata['description']=request.POST['description']
            initialdata['created_date']=datetime.now()
            form=CreateTicketForm(initialdata)
            print form.data    
            if form.is_valid():
                try:
                    form.save(commit=True)
                    status="form kaydedildi"
                except Exception as e:
                    status="hata olustu"
                    print e
            else:
                print "form kaydedilemedi"
        else:
            form = CreateTicketForm()
        return render_to_response('createticket.html', {'form':form,'status':status})

@login_required
def view_dashboard(request):
    tickets = Ticket.objects.filter(createdbyUser=request.user)
    return render_to_response('mytickets.html', {'tickets':tickets})

@login_required
def showticket(request,ticket_id):
    ticket = Ticket.objects.filter(pk=ticket_id)
    return render_to_response('ticketdetails.html',{'ticket':ticket})

def index(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect("/accounts/login")
    else:
        return HttpResponseRedirect(reverse("view_dashboard"),{'user':request.user})

