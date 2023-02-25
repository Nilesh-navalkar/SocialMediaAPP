from django.shortcuts import render,redirect
from django.contrib.auth import login as li,authenticate,logout
from django.contrib import messages
from django.contrib.auth.models import User
from .models import profile,bio,post,follow
from django.contrib.auth.decorators import login_required
from datetime import datetime
# Create your views here.

def landing(request):
    return render(request,"landing.html")

@login_required(login_url="login")
def search(request):
    if request.method=='POST':
        f=request.POST.get('f')
        #print(f)
        x=bio.objects.filter(un=f).values_list("name","country","un")
        #print(list(x))
        if x:
            return render(request,"search.html",{'x':list(x)})
        else:
            messages.error(request,"no user exists")
            return render(request,"search.html")
    return render(request,"search.html")

@login_required(login_url="login")
def flow(request,un):
    u=request.user.username
    f=un
    #print(f)
    if f:
        if f==u:
            messages.error(request,"cant follow yourself")
        elif follow.objects.filter(u=u,f=f).exists():
            messages.error(request,"You already follow this user")
        else:
            follow.objects.create(u=u,f=f)
            messages.error(request,"followed")
            
        return redirect("search")

    return render(request,"search.html")

@login_required(login_url="login")
def home(request):
    if request.method=="POST":
        p=request.FILES.get("pp")
        if p:
            post.objects.create(u=request.user,s=request.user.username,newpost=p,t=datetime.now())
            messages.error(request,"Post Uploaded")
            return redirect("home")
        else:
            messages.error(request,"choose a file to upload")
            return redirect("home")
    u=request.user.username
    f=follow.objects.filter(u=u).values_list()
    #print(f)
    show=[]
    for i in f:
        s=post.objects.filter(s=i[2]).values_list('newpost','s')
        # print(list(s))
        for k in s:
            show.append(("media/"+k[0],k[1]))
            
    #print(show)
    return render(request,"home.html",{'show':show})

@login_required(login_url="login")
def profile1(request):
    f1=follow.objects.filter(u=request.user.username).values_list()
    f2=follow.objects.filter(f=request.user.username).values_list()
    s=bio.objects.filter(u=request.user).values()
    if s:
        d=s[0]
        d['profilepic']="media/"+d['profilepic']
        d['email']=request.user.email
        #print(d['profilepic'])
        #print(request.user)
        if post.objects.filter(u=request.user).exists():
            qs=post.objects.filter(u=request.user).values_list()
            posts=[]
            l=0
            for i in qs:
                l=l+1
                posts.append("media/"+i[3])
            #print(qs)
            d['l']=l
            d['posts']=posts
        d['f1']=len(f1)
        d['f2']=len(f2)
        return render(request,"profile.html",d)
    return render(request,"profile.html")

@login_required(login_url="login")
def settings(request):
    if request.method=="POST":
        name=request.POST.get("name")
        b=request.POST.get("bio")
        country=request.POST.get("c")
        no=request.POST.get("no")
        dob=request.POST.get("dob")
        pp=request.FILES.get("pp")
        #print(name,bio,no,dob,country,pp)
        if bio.objects.filter(u=request.user).exists():
            ebio = bio.objects.get(u=request.user)
            if name:
                ebio.name = name
            if b:
                ebio.b=b
            if country:
                ebio.country=country
            if no:
                ebio.phone=no
            if dob:
                ebio.dob=dob
            if pp:
                ebio.profilepic=pp
            ebio.save()
            messages.error(request,"Profile Updated.")
            return redirect("settings")
        else:
            newbio=bio.objects.create(u=request.user,b=b,name=name,country=country,phone=no,dob=dob,profilepic=pp,un=request.user.username)
            newbio.save()
            messages.error(request,"Profile Updated.")
            return redirect("settings")
    return render(request,"settings.html")

def signup(request):
    if request.method=="POST":
        name=request.POST.get("name")
        email=request.POST.get("email")
        p1=request.POST.get("p1")
        p2=request.POST.get("p2")
        #print(email)
        if p1!=p2:
            messages.error(request,"passwords dont match")
            #print("redictred")
            return redirect("signup")
        elif User.objects.filter(username=name).exists():
            messages.error(request,"username already exits")
            return redirect("signup")
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email taken")
            return redirect("signup")
        else:
            u=User.objects.create_user(username=name,email=email,password=p1)
            u.save()
            um=User.objects.get(username=name)
            addprofile=profile.objects.create(u=um,email=email)
            addprofile.save()
            blankbio=bio.objects.create(u=um)
            blankbio.save()
            return redirect("login")
    return render(request,"signup.html")

def login(request):
    if request.method=="POST":
        un=request.POST.get("un")
        p=request.POST.get("p")
        user=authenticate(username=un,password=p)
        #print(user,un)
        if user is not None:
            li(request,user)
            return redirect("settings")
        else:
            messages.error(request,"invalid credentials")
            return redirect("login")
            
    return render(request,"login.html")

@login_required(login_url="login")
def log_out(request):
    logout(request) 
    return redirect("login")




