from django.http import HttpResponseRedirect
from django.shortcuts import render
from .models import Chat, Message
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received data: " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, "chat/index.html", {'messages': chatMessages})

def login_view(request):
    redirect = request.POST.get('redirect')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})

def register_view(request):
    if request.method == 'POST':
        email_exists = User.objects.filter(email=request.POST.get('email')).exists()
        if email_exists == False:
            User.objects.create_user(username = request.POST.get('username'), email = request.POST.get('email'),password = request.POST.get('password'))
            return HttpResponseRedirect('/login/')
        else:
            return render(request, 'auth/register.html', {'unavailableAccount': True})
    return render(request, 'auth/register.html')