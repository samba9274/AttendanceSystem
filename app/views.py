from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import User
def home(request):
    return redirect('/login')
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if(User.objects.filter(email=email).exists()):
            user = User.objects.get(email=email)
            if user.password == password:
                if user.role=='teacher' or user.role == 'admin':
                    response = redirect('/dashboard')
                else:
                    response = redirect('/dashboard')
                response.set_cookie('email', user.email)
                response.set_cookie('name', user.name)
                response.set_cookie('role', user.role)
                response.set_cookie('attendance', user.attendance)
                return response
            else:
                messages.info(request, 'Incorrect password')
            return redirect('/login')
        else:
            messages.info(request, 'User not found. Try registering')
            return redirect('/login')
    return render(request, 'login.html')
def logout(request):
    response = redirect('/login')
    response.delete_cookie('email')
    response.delete_cookie('name')
    response.delete_cookie('role')
    response.delete_cookie('attendance')
    return response
def register(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email taken')
            return redirect('/register')
        else:
            User.objects.create(name=name, email=email, password=password, role='student', attendance='absent').save()
            return redirect('/login')
    return render(request, 'register.html')
def dashboard(request):
    if request.COOKIES.get('email') and request.COOKIES.get('name') and request.COOKIES.get('role') and request.COOKIES.get('attendance'):
        if request.COOKIES.get('role') == 'teacher' or request.COOKIES.get('role') == 'admin':
            return render(request, 'dashboard.html', context={'name':request.COOKIES.get('name'), 'role':request.COOKIES.get('role'), 'attendance':request.COOKIES.get('attendance'), 'students':list(User.objects.filter(role='student'))})
        return render(request, 'dashboard.html', context={'name':request.COOKIES.get('name'), 'role':request.COOKIES.get('role'), 'attendance':request.COOKIES.get('attendance')})
    return redirect('/login')
def requestAttendance(request):
    response = redirect('/dashboard')
    if request.COOKIES.get('email') and request.COOKIES.get('name') and request.COOKIES.get('role') and request.COOKIES.get('attendance'):
        if User.objects.filter(email=request.COOKIES.get('email')).exists():
            if request.COOKIES.get('role') == 'student':
                user = User.objects.get(email=request.COOKIES.get('email'))
                user.attendance='requested'
                response.set_cookie('attendance', 'requested')
                user.save()
            else:
                messages.info(request, 'Not a student')
        else:
            messages.info(request, 'User not found')
    else:
        messages.info(request, 'Not logged in')
    return response
def acceptAttendance(request):
    response = redirect('/dashboard')
    if User.objects.filter(email=request.GET.get('email')).exists():
        user = User.objects.get(email=request.GET.get('email'))
        if user.role == 'student':
            user.attendance = 'present'
            user.save()
    return response