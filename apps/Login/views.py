from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.db import connection, transaction
from django.contrib import messages


cursor = connection.cursor()

def index(request):
    User.objects.all()
    context={
        "users":User.objects.all()
    }
    return render(request, 'index.html')
def login(request):
    context={
        "users":User.firstname

    }
    errors = User.objects.validate_log(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags=field)
        
        return redirect('/')
    else:

        return render(request, 'login.html', context)
    return redirec('/')
def register(request, id):
    context={
        "users":User.objects.get(id=id)
    }
    errors = User.objects.validate_reg(request.POST)
    if len(errors):
        for field, message in errors.iteritems():
            messages.error(request, message, extra_tags=field)
        
        return redirect('/')
    else:
        hash1 = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        users=User.objects.create(firstname=request.POST['firstname'], lastname=request.POST['lastname'],email=request.POST['email'], password=hash1)
        

        return render(request, 'register.html', context )
    return redirect('/')
# Create your views here.
