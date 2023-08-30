import os
from django.shortcuts import redirect, render
from django.contrib.auth.models import User,auth
from myapp.models import Course,Student,Details
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login

# Create your views here.

def home(request):
    return render(request,'home.html')

def signin(request):
    return render(request,'signin.html')

def signup(request):
    stud=Course.objects.all()
    return render(request,'signup.html',{'courses':stud})

@login_required(login_url='signin')
def course(request):
    return render(request,'addcourse.html')

@login_required(login_url='signin')
def addstudent(request):
    stud=Course.objects.all()
    return render(request,'addstudent.html',{'courses':stud})

@login_required(login_url='signin')
def teacherhome(request):
    return render(request,'teacherhome.html')

@login_required(login_url='signin')
def adminhome(request):
    return render(request,'adminhome.html')

def log(request):
    if request.method == 'POST':
        username=request.POST['uname']
        password=request.POST['password']
        admin=auth.authenticate(username=username, password=password)
        
        if admin is not None:
            if admin.is_staff:
                login(request,admin)
                return redirect('adminhome')
            else:
                login(request,admin)
                auth.login(request,admin)
                messages.info(request, f'Welcome {username}')
                return redirect('teacherhome')
        else:
            messages.info(request, 'Invalid Username or Password. Please Try Again.')
            return redirect('signin')
    else:
        return redirect('signin')

def add_course(request):
    if request.method == "POST":
        cname=request.POST['cname']
        fees=request.POST['fees']
        cou=Course(course_name=cname,fees=fees)
        cou.save()
        return redirect('course')
    
def add_student(request):
    if request.method == "POST":
        sname=request.POST['sname']
        age=request.POST['age']
        address=request.POST['address']
        sel=request.POST['sel']
        course=Course.objects.get(id=sel)
        stu=Student(sname=sname,age=age,address=address,course=course)
        stu.save()
        return redirect('student_det')
    return redirect('addstudent')

def add_teacher(request):
    if request.method=='POST':
        first_name=request.POST['fname']
        last_name=request.POST['lname']
        mob=request.POST['mob']
        address=request.POST['address']
        username=request.POST['uname']
        email=request.POST['mail']
        image = request.FILES.get('file')
        sel=request.POST['sel']
        course=Course.objects.get(id=sel)
        password=request.POST['password']
        cpassword=request.POST['cpassword']

        if password==cpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, 'This username already exists')
                return redirect('signin')
            else:
                user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,password=password,email=email)
                user.save()
                det=Details(mob=mob,address=address,course=course,user=user,image=image)
                det.save()
        else:
            messages.info(request, "Password doesn't match")
            return redirect('signin')   
        return redirect('signin')
    else:
        return render(request,'signin.html')

def student_det(request):
    stud=Student.objects.all()
    return render(request,'student_details.html',{'studen':stud})

def teacher_det(request):
    stud=Details.objects.all()
    return render(request,'teacher_det.html',{'studen':stud})

def delete_teacher(request,pk):
    det=Details.objects.get(user=pk)
    det.delete()
    u=User.objects.get(id=pk)
    u.delete()   
    return redirect('teacher_det')

def delete_student(request,pk):
    det=Student.objects.get(id=pk)
    det.delete()   
    return redirect('student_det')

@login_required(login_url='signin')
def edit_student(request,pk):
    stud=Student.objects.get(id=pk)
    cou=Course.objects.all()
    return render(request,'edit_student.html',{'student':stud,'courses':cou})

def edit_stu(request,pk):
    if request.method == "POST":
        stu=Student.objects.get(id=pk)
        stu.sname=request.POST['sname']
        stu.address=request.POST['address']
        stu.age=request.POST['age']
        sel=request.POST['sel']
        course1=Course.objects.get(id=sel)
        stu.course=course1
        stu.save()
        return redirect('student_det')
    return redirect('/')

@login_required(login_url='signin')
def tedit(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        user1=Details.objects.get(user=current_user)
        user2=User.objects.get(id=current_user)
        stud=Course.objects.all()
        if request.method=='POST':
            if len(request.FILES)!=0:
                if len(user1.image)>0:
                    os.remove(user1.image.path)
                user1.image=request.FILES.get('file')
            user2.first_name=request.POST['fname']
            user2.last_name=request.POST['lname']
            user1.mob=request.POST['mob']
            user1.address=request.POST['address']
            user2.username=request.POST['uname']
            user2.email=request.POST['mail']
            sel=request.POST['sel']
            course1=Course.objects.get(id=sel)
            user1.course=course1
            user1.save()
            user2.save()
            return redirect('profile')

        return render(request,'edit_teacher.html',{'users':user1,'courses':stud})
    return redirect('/')
    

@login_required(login_url='signin')
def profile(request):
    if request.user.is_authenticated:
        current_user=request.user.id
        user1=Details.objects.get(user=current_user)
        return render(request,'tprofile.html',{'users':user1})

@login_required(login_url='signin')
def logout(request):
    #if request.user.is_authenticated:
    #request.session["uid"]=""
    auth.logout(request)
    return redirect('home')
