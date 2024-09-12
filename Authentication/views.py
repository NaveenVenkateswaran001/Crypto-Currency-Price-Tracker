from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import login,logout
# Create your views here.
def loginForm(request):
     
     if request.user.is_authenticated:
          login(request,request.user)
          return render(request,'home.html')
     
     if request.method == 'POST':
          userName = request.POST['username'].lower()
          password = request.POST['password']
          try:
               user = User.objects.get(username = userName)
               if user.check_password(password):
                    login(request,user)
                    return render(request,'home.html')
               else:
                    return render(request,'signin.html',{'invalid':'Incorrect Password'})
          except:
               return render(request,'signin.html',{'notExist':'*Username does not exist'})
     else :               
          return render(request,'signin.html')


def signupForm(request):
     if request.method == 'POST':
          userName = request.POST['username'].lower()
          passWord = request.POST['password']
          email = request.POST['email']
          
          existing_userName = User.objects.filter(username = userName)
          existing_email = User.objects.filter(email = email).exists()
          
          if existing_userName and existing_email:
               return render(request,'signup.html',{'email_exist':'*Username and Email already exist'})
          elif existing_userName:
               return render(request,'signup.html',{'email_exist':'*Username already exists'})
          elif existing_email:
               return render(request,'signup.html',{'email_exist':'*Email address already exists'})
               
          try:
               existing_user = User.objects.get(username = userName)  
               return render(request,'signup.html',{'exist':'*Username already exists'})
          
          except:
               new_user = User(
                    username = userName,
                    first_name = request.POST['firstname'],
                    last_name = request.POST['lastname'],
                    email = request.POST['email']
                    )
               new_user.set_password(passWord)
               new_user.save()
               login(request,new_user)
               return render(request,'home.html')
          
     else:
          return render(request,'signup.html')          

 
def logoutForm(request):
     logout(request)
     return redirect('loginForm')             
