from django.shortcuts import render, redirect
from .models import Board, Reply
from django.utils import timezone
from django.core.paginator import Paginator
from django.contrib import messages


# Create your views here.
def unlikey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.remove(request.user)
    return redirect("board:detail", bpk)

def likey(request, bpk):
    b = Board.objects.get(id=bpk)
    b.likey.add(request.user)
    return redirect("board:detail", bpk)

def dreply(request, bpk, rpk):
    r = Reply.objects.get(id=rpk)
    if request.user == r.replyer:
        r.delete()
    else:
        pass
    return redirect("board:detail", bpk)

    
def creply(request, bpk):
    b = Board.objects.get(id=bpk)
    c = request.POST.get("com")
    p = timezone.now()
    Reply(board=b, replyer=request.user, comment=c, pubdate=p).save()
    return redirect("board:detail", bpk)


def update(request, bpk):
    b = Board.objects.get(id=bpk)

    if request.user != b.writer:
        return redirect("board:index")

    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        b.subject, b.content = s, c 
        b.save()
        return redirect("board:detail", bpk)

    context = {
        'b' : b
    }
    return render(request, "board/update.html", context)


def create(request):
    if request.method == "POST":
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
        return redirect("board:index")
    return render(request, "board/create.html")


def delete(request, bpk):
    b = Board.objects.get(id=bpk)
    if request.user == b.writer:
        b.delete()
        return redirect("board:index")
    else:
        messages.error(request, "한번만 더 걸리면 죽는다^^")
        return redirect("board:detail")


def detail(request, bpk):
    b = Board.objects.get(id=bpk)
    r = b.reply_set.all()
    r = r.order_by("-pubdate")
    context = {
        'b' : b,
        'rset' : r
    }
    return render(request, "board/detail.html", context)


def index(request):
    kw = request.GET.get("kw", "")
    cate = request.GET.get("cate", "")
    page = request.GET.get("page", 1) 

    if kw:
        if cate == "sub":
            b = Board.objects.filter(subject__startswith = kw).order_by('-pubdate')
        elif cate == "wri":
            try:
                from acc.models import User
                u = User.objects.get(username=kw)
                b = Board.objects.filter(writer=u).order_by('-pubdate')
            except:
                b = Board.objects.none()
        elif cate == "con":
            b = Board.objects.filter(subject__contains = kw).order_by('-pubdate')
        else:
            b = Board.objects.all().order_by('-pubdate')
    else:
        b = Board.objects.all().order_by('-pubdate')

    pag = Paginator(b, 4)

    obj = pag.get_page(page)

    context = {
        'bset' : obj,
        'kw' : kw,
        'cate' : cate
    }
    return render(request, "board/index.html", context)
