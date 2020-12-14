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

def detail(request, article_id):
    try:
        check = False
        article = Article.objects.get(id=article_id)
        if request.user.is_authenticated:
            profile = Profile.objects.get ( user = request.user.id )
            if str(article.article_title) not in profile.featured_articles_list:
                check = True
        else:
            profile = None
        last_comments = article.comment_set.order_by('-id')[:10]
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return render(request, 'detail.html', {'article': article,'last_comments':last_comments,'check':check })

def add_comment(request,article_id,nickname):
    try:
        article = Article.objects.get(id=article_id)
        if request.POST['text']  != '' and request.POST['text']  != ' ':
            profile = Profile.objects.get(user = request.user.id)
            ##link = '/profile/' + str(User.objects.get(id = request.user.id))
            article.comment_set.create(comment_title = nickname,comment_text = request.POST['text'],comment_author_image = profile.profile_avatar , author_id = request.user.id )
        else:
            error_msg = 'You can`t sand null massage'
    except Article.DoesNotExist:
        raise Http404("Article does not exist")
    return HttpResponseRedirect(reverse('detail', args=(article.id,)))


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
    return render(request,'profile.html',context)



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
                    return render(request,'registration/register.html',{'error_msg' : error_msg})

                if User.objects.filter(username = username):
                    error_msg = 'Логин уже занят'
                    return render(request,'registration/register.html',{'error_msg' : error_msg})

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
                return render(request,'profile.html',context)
            else:
                error_msg = 'Некорректный логин или пароль или никнейм '
                return render(request,'registration/register.html',{'error_msg' : error_msg})
        else:
            error_msg = 'Пароли не совпадают'
            return render(request,'registration/register.html',{'error_msg' : error_msg})

    else:
        return render(request,'registration/register.html')

def search(request):
    searched_article = request.POST['search']
    append_list = []
    append_people_list = []
    article_list = Article.objects.all()
    for i in article_list:
        i_new = str(i).lower()
        for a in i_new.split():
            for x in searched_article.lower().split():
                if a.startswith(x):
                    append_list.append(i)
    if not append_list:
        people_list = User.objects.all()
        for i in people_list:
            for a in searched_article.lower().split():
                if str(i).lower().startswith(a):
                    append_people_list.append(i)

    context = {
        'append_list' : append_list ,
        'append_people_list' : append_people_list
    }
    return render(request,'searched_articles.html',context)

def add_article_list(request , article_id):
    profile = Profile.objects.get ( user = request.user.id )
    article = Article.objects.get ( id = article_id)
    if str(article) not in profile.featured_articles_list:
        profile.featured_articles_list += ('/' + str(article))
        profile.save()
    return HttpResponseRedirect(reverse('detail', args=(article.id,)))

def featured_article(request,user_id):
    featured_list = []
    user2 = User.objects.get( id = user_id )
    profile = Profile.objects.get(user = user_id )
    if profile.featured_articles_list:
        for i in profile.featured_articles_list.split('/'):
            try:
                succes = Article.objects.get( article_title = i)
                featured_list.append(succes)
            except:
                continue
    context = {
        'profile': profile,
        'featured_list' : featured_list,
        'user2':user2
    }
    return render(request,'featured_articles.html',context)