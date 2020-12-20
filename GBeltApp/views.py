from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages


def index(request):
    return render(request, "index.html")


def registerUser(request):
    errorsFromNewUser = User.objects.userValidation((request.POST))
    if len(errorsFromNewUser) > 0:
        for key, value in errorsFromNewUser.items():
            messages.error(request, value)
        return redirect("/")
    else:
        newUser = User.objects.create(first_name=request.POST['fname'],
                                      last_name=request.POST['lname'],
                                      email=request.POST['email'],
                                      password=request.POST['pw'])
        request.session['loggedInId'] = newUser.id

    return redirect("/quotes")


def login(request):
    resultFromVal = User.objects.loginValidation(request.POST)
    print(resultFromVal)
    if len(resultFromVal) > 0:
        for key, value in resultFromVal.items():
            messages.error(request, value)
        return redirect("/")
    else:
        matchingemail = User.objects.filter(email=request.POST['logemail'])
        request.session['loggedInId'] = matchingemail[0].id
    return redirect('/quotes')


def home(request):
    if 'loggedInId' not in request.session:
        return redirect("/")
    context = {
        'loggedInUser': User.objects.get(id=request.session['loggedInId']),
        'quotesLeft': Quote.objects.all(),
    }
    return render(request, "home.html", context)


def logout(request):
    request.session.clear()
    return redirect("/")


def editAcc(request, idShow):
    if 'loggedInId' not in request.session:
        return redirect("/")
    context = {
        'idToSchow': User.objects.get(id=idShow)
    }
    return render(request, 'editAcc.html', context)


def updateUser(request, idShow):
    errorsFromEditUser = User.objects.editValidation((request.POST))
    if len(errorsFromEditUser) > 0:
        for key, value in errorsFromEditUser.items():
            messages.error(request, value)
        return redirect(f"/myaccount/{idShow}")
    else:
        user = User.objects.get(id=idShow)
        user.first_name = request.POST['fname']
        user.last_name = request.POST['lname']
        user.email = request.POST['email']
        user.save()
    return redirect('/quotes')


def addPost(request):
    print(request.POST)
    Quote.objects.create(author=request.POST['author'],
                         content=request.POST['desc'],
                         poster=User.objects.get(id=request.session['loggedInId']))
    return redirect('/quotes')


def userInfo(request, idShow):
    content = {
        'idToUser': User.objects.get(id=idShow),
    }
    return render(request, "user.html", content)


def deletePost(request, idShow):
    delPost = Quote.objects.get(id=idShow)
    delPost.delete()
    return redirect('/quotes')


def likePost(request, idShow):
    this_User = User.objects.get(id=request.session['loggedInId'])
    this_post = Quote.objects.get(id=idShow)
    this_post.likes.add(this_User)

    return redirect('/quotes')


def unlikePost(request, idShow):
    this_User = User.objects.get(id=request.session['loggedInId'])
    this_post = Quote.objects.get(id=idShow)
    this_post.likes.remove(this_User)

    return redirect('/quotes')
