from django.shortcuts import render
from django.http import HttpResponse , Http404 , HttpResponseRedirect
from django.contrib.auth.models import User
from .models import Article,Comment,Profile 
from .forms import ProfileForm
from django.urls import reverse
from django.contrib import auth
from django.views.decorators.csrf import ensure_csrf_cookie
import re

def index(request):
    user2 = None
    if request.user.is_authenticated:
        user2 = User.objects.get(id = request.user.id)
    last_article_list = Article.objects.order_by('-date_publish')[:5]
    return render(request,'index.html',{'last_article_list':last_article_list,'user2':user2,})

def profile(request,user_id):
    user2 = User.objects.get( id = user_id )
    profile = Profile.objects.get(user = user_id )
    form = ProfileForm( request.POST or None , request.FILES or None ,  instance=profile )
    if form.is_valid():
        form.save()
    context = {
        'form' : form ,
        'profile': profile,
        'user2' : user2,
    }
    return render(request,'SimpleBlog/profile.html',context)



def register(request):
    error_msg = None
    user2 = None
    if request.method == 'POST':
        if request.POST['password'] == request.POST['password1']:
            username = request.POST['username']
            password = request.POST['password']
            nickname = request.POST['nickname']
            if re.match(r'^\D{3}\w{2,12}', username) and re.match(r'^\S{6,20}',password) and re.match(r'^\D{3}\w{2,12}',nickname):
                if User.objects.filter(first_name = nickname):
                    error_msg = 'Никнейм уже занят'
                    return render(request,'SimpleBlog/registration/register.html',{'error_msg' : error_msg})

                if User.objects.filter(username = username):
                    error_msg = 'Логин уже занят'
                    return render(request,'SimpleBlog/registration/register.html',{'error_msg' : error_msg})

                user = User.objects.create_user(username = username , first_name = nickname ,password = password)
                user.save()
                user2 = auth.authenticate(username=username, password=password)
                auth.login(request, user2)
                profile = Profile.objects.get( user = user2.id )
                profile.featured_articles_list = '/'
                profile.save()
                form = ProfileForm( request.POST or None , request.FILES or None ,  instance=profile )
                if form.is_valid():
                    form.save()
                context = {
                    'form' : form ,
                    'profile': profile,
                    'user2': user2,
                }
                return render(request,'SimpleBlog/profile.html',context)
            else:
                error_msg = 'Некорректный логин или пароль или никнейм '
                return render(request,'SimpleBlog/registration/register.html',{'error_msg' : error_msg})
        else:
            error_msg = 'Пароли не совпадают'
            return render(request,'SimpleBlog/registration/register.html',{'error_msg' : error_msg})

    else:
        return render(request,'SimpleBlog/registration/register.html')