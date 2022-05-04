import os

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import User,Posts,Tag,UserDetails
from django.contrib.auth.decorators import login_required,user_passes_test
# Create your views here.
def home(request):
    return render(request,'home.html')

def sign_up(request):
    return render(request,'sign_up.html')


def create_user(request):

    if request.method == "POST":
        username = request.POST['username']
        firstname = request.POST['first_name']
        last_name = request.POST['last_name']
        password= request.POST['password']
        email= request.POST['email']
        obj = User.objects.create(username=username,first_name= firstname,last_name=last_name,password=password,email=email)
        obj.save()
        user = User.objects.get(username=username)
        userdetails = UserDetails.objects.create(user=user)
        userdetails.save()
        return redirect('/')
    return redirect('/')

def add_post(request):

    if request.method == "POST":
        username = request.session['username']
        # title = request.POST['title']
        poster = request.FILES['poster']
        description = request.POST['description']
        try:
            user= User.objects.get(username=username)
            obj = Posts.objects.create( description=description,poster=poster,created_by=user)
            # obj.tags.set([tags])
            obj.save()
        except Exception as e:
            print(e)
            messages.error(request, 'Failed to upload')
            return redirect('/')
        def extract_hashtags(text):

            # initializing hashtag_list variable
            hashtag_list = []

            # splitting the text into words
            for word in text.split():

                # checking the first character of every word
                if word[0] == '#':
                    # adding the word to the hashtag_list
                    hashtag_list.append(word[1:])

            # printing the hashtag_list
            print("The hashtags in \"" + text + "\" are :")
            for hashtag in hashtag_list:
                print(hashtag)

        return redirect('/show_posts')
    return render(request,'add_post.html')


def show_posts(request):
    posts = Posts.objects.all().order_by('-created_at')
    context ={"posts":posts}
    return render(request,'show_posts.html', context)


def log_in(request):
    if request.method == "POST":
        username= request.POST["username"]
        password = request.POST["password"]
        user = User.objects.all().filter(username=username)

        if user:
            if user[0].password == password:
                request.session["username"]=username
                request.session['isLoggedIn']=True
                return HttpResponseRedirect('/show_posts')
            else:
                return render(request,'log_in.html', {"error":"Invalid password"})
        else:
            return render(request, 'log_in.html', {"error": "Username Invalid"})
    else:
        return render(request,"log_in.html")

def log_out(request):
    request.session["isLoggedIn"] = False
    request.session['username']=""
    return HttpResponseRedirect('/show_posts')

def account(request):
    try:
        username= request.session["username"]
        print(username)
        user = User.objects.get(username=username)
        userdetails = UserDetails.objects.get(user=user)
        # print(userdetails.profile_picture)
        posts = Posts.objects.all().filter(created_by=user.id).order_by('-created_at')

        context = {"posts": posts,
                   "userinfo":user,
                   "userdetail":userdetails
                   }
        return render(request,"account.html",context)
    except Exception as e:
        print(e)
        messages.error(request, 'Not Logged in.')
        return redirect("/show_posts")

def update_profile(request):

        if request.method == "POST":
            print("in post method")
            username = request.session["username"]
            firstname = request.POST['first_name']
            last_name = request.POST['last_name']
            password = request.POST['password']

            mobile = request.POST['mobile']

            email = request.POST['email']
            obj = User.objects.filter(username=username).update(first_name=firstname, last_name=last_name,email=email,password=password)

            user = User.objects.get(username=username)
            obj2 = UserDetails.objects.get(user=user)
            obj2.mobile = mobile
            # obj2.is_active=status
            if len(request.FILES) != 0:
                if len(obj2.profile_picture) > 0:
                    if(obj2.profile_picture!="imgs/usericonblue.png"):
                        thisdir=os.getcwd()
                        pic=str(obj2.profile_picture)

                        os.remove(thisdir+'/static/'+pic)
                obj2.profile_picture = request.FILES['profile_picture']

            obj2.save()



            print("updated")
            return redirect('/show_posts')
        if request.method == "GET":

            username = request.session["username"]
            user = User.objects.get(username=username)
            userdetails = UserDetails.objects.get(user=user)
            context = {
                       "userinfo":user,
                       "userdetail": userdetails
                       }
            return render(request, "update_profile.html", context)

def delete_post(request):
    if request.method == "POST":
        username = request.session["username"]
        if(username):
            post_details = request.POST["post_details"]
            post = Posts.objects.get(id=post_details)
            if len(post.poster) > 0:
                thisdir = os.getcwd()
                pic = str(post.poster)
                os.remove(thisdir + '/static/' + pic)
            post.delete()
            return redirect('/user/account')
        else:
            messages.error(request, 'Failed to delete')
            return redirect('/show_posts')

