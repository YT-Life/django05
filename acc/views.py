from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from .models import User
from django.contrib import messages

# Create your views here.
def update(request):
    if request.method == "POST":
        u = request.user
        up = request.POST.get("upass")
        um = request.POST.get("umail")
        uc = request.POST.get("ucom")
        upic = request.FILES.get("upic")
        if up:
            u.set_password(up)
        u.email = um
        u.comment = uc
        if upic:
            u.pic.delete()
            u.pic = upic
        u.save()
        login(request, u)
        return redirect("acc:profile")

    return render(request, "acc/update.html")

def delete(request):
    ck = request.POST.get("pwck")
    if check_password(ck, request.user.password):
        request.user.pic.delete()
        request.user.delete()
        return redirect("acc:index")
    else:
        messages.error(request, "비밀번호가 일치하지 않습니다.")
        return redirect("acc:profile")
        
        
def profile(request):
    return render(request, "acc/profile.html")

def userlogout(request):
    logout(request)
    return redirect("acc:index")


def signup(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        uc = request.POST.get("ucom")
        upic = request.FILES.get("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, pic=upic)
            return redirect("acc:login")
        except:
            messages.error(request, "ID가 이미 사용중입니다.")
    return render(request, "acc/signup.html")

def userlogin(request):
    if request.method == "POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        user = authenticate(username=un, password=up)
        if user:
            login(request, user)
            messages.success(request, f"{user}님 환영합니다.")
            return redirect("acc:index")
        else:
            messages.error(request, "ID 및 PASSWORD가 일치하지 않습니다.")
    return render(request, "acc/login.html")

def index(request):
    return render(request, "acc/index.html")