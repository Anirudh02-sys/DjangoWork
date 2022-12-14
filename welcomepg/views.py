from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User,Act
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from .forms import UploadFileForm
# Create your views here.
def loginpage(request):
    if(request.method =='POST'):
        user = authenticate(username=request.POST['u'], password=request.POST['p'])
        if user is not None:
            login(request,user)
            return redirect('/home')
        else:
            messages.info(request,'invalid credentials!')
            return redirect('/')
    # No backend authenticated the credentials
    else:
        return(render(request,'loginpage.html'))

def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST,request.FILES)
        file = request.FILES['file']
        file.save()
        return HttpResponse("The name of the uploaded file is" + str(file))
    else:
        form = UploadFileForm()
    return render(request,'upload.html',{'form':form})        

def home(request):
    if request.user.is_superuser:
        return render(request,'adminpage.html')
    elif request.user.role == 'Subcontractor':
        return render(request,'subcont.html')
    elif request.user.role == 'Auditor':
        return render(request,'auditpage.html')



def events(request):
    return render(request,'createevent.html')  
    
def actmaster(request):
    act = Act.objects.all()
    return render(request,'actmaster.html',{'act': act})

def userlist(request):
    userl = User.objects.all()
    return render(request,'userlist.html',{'userl': userl})    

def newact(request):
    if (request.method == 'POST'):
        act_name = request.POST['actn']
        act_desc = request.POST['actd']
        act_sname = request.POST['actsn']
        actsdata = Act.objects.create(act_name = act_name, act_shname = act_sname,act_desc=act_desc)
        actsdata.save()

        return render(request,'actmaster.html')
    else:
        return render(request,'newact.html')  



def createnewuser(request):
    auditors = User.objects.filter(role='Auditor')
    context = {'auditors':auditors}
    if (request.method == 'POST'):
        print(request.POST['choose'])
        first_name = request.POST['fname']
        last_name =  request.POST['lname']
        username = request.POST['usr']
        email = request.POST['email']
        password1 = request.POST['psw']
        password2 = request.POST['psw-repeat']
        contact_number = request.POST['telphone']
        role = request.POST['choose']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken!')
                return redirect('createnewuser')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'E-mail Taken!')
                return redirect('createnewuser')
            else:
                print("hey")
                user = User.objects.create_user(username=username,password=password1,email=email,first_name=first_name,last_name=last_name,role=role,contact_number=contact_number)
                user.save()
                '''
                if allot:
                    alloted = Allot.objects.create(contractor= User.objects.filter(username = username))
                    alloted.auditor = User.objects.filter(username = allot)
                    alloted.save()
                messages.success(request,'User Sucessfully created')
                '''
        else:
            messages.info(request,'Password not matching!')
            return redirect('createnewuser')
    
        return redirect('createnewuser')
    else:
        return render(request,'createnewuser.html',context)

def logoutpage(request):
    logout(request)
    return redirect('login')        

