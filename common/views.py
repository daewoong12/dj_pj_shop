from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login
from common.forms import UserForm
from mall.models import Cart
from mall.models import Stuff
from django.contrib.auth import logout
# Create your views here.

def signup(request):
    if request.method=="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data.get('username')
            raw_password=form.cleaned_data.get('password1')
            user=authenticate(username=username,password=raw_password)
            login(request,user)
            # stuffs = Stuff()
            # thisCart=Cart(user=user,stuffs=stuffs)
            # thisCart.save()
            # thisCart.user.add(request.user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request,'common/signup.html',{'form':form})

def custom_logout(request):
    logout(request)
    return redirect('common:login')  # 로그아웃 후 로그인 페이지로 리다이렉트


