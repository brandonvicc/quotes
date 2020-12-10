from django.shortcuts import render, redirect
from .models import User, Quote
from django.contrib import messages
import bcrypt
from django.db.models import Count

# Create your views here.
def root(request):
    return render(request,'root.html')

def create(request):
    if request.method == "POST":
        errors = User.objects.create_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode() 
            user = User.objects.create(first_name= request.POST['first_name'], last_name= request.POST['last_name'], email= request.POST['email'], password = pw_hash)
            request.session['user_id'] = user.id #important!
    return redirect('/quotes')

def login(request):
    if request.method == 'POST':
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
            return redirect('/')
        else:
            user = User.objects.filter(email= request.POST['email'])
            if user:
                logged_user = user[0]
                if bcrypt.checkpw(request.POST['password']. encode(), logged_user.password.encode()):
                    request.session['user_id'] = logged_user.id
                    return redirect('/quotes')
                else: 
                    print("Password didn't Match")
                    messages.error(request, "Incorrect name or password")
            else:
                print('Name not fount')
                messages.error(request, "Incorrect name or password")
    return redirect('/')

def logout(request):
    if request.method == "POST":
        request.session.clear()
    return redirect("/")

def quotes(request):
    if request.method == 'GET':
        if "user_id" in request.session:
            user = User.objects.get(id=request.session['user_id'])
            context = {
                "likes" : Quote.objects.annotate(likes=Count('user_likes')),
                'user': user,
                "quotes": Quote.objects.all()
                }
            return render(request,'quotes.html', context)
        else:
            return redirect('/')

def create_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
        else:
            Quote.objects.create(author_by = request.POST['author_by'], quote= request.POST['quote'], posted_by = User.objects.get(id = request.session['user_id']))
    return redirect('/quotes')

def profile(request,id):
    if request.method == 'GET':
        if "user_id" in request.session:
            user_selected = User.objects.filter(id=id)
            if user_selected:
                user = user_selected[0]
                context = {
                    "user" : user
                }
                return render(request,"profile.html", context)
        else:
            return redirect('/quotes')

def edit(request,id):
    if "user_id" in request.session:
        user_selected = User.objects.filter(id=id)
        if user_selected:
            user = user_selected[0]
            context = {
                "user" : user
            }
            return render(request,"edit_profile.html", context)
    else:
        return redirect('/quotes')

def update(request,id):
    if request.method == 'POST':
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request,value)
                return redirect(f'/edit/{id}')
        else:
            update_this_user = User.objects.filter(id=id)
            if update_this_user:
                update_this = update_this_user[0]
                user = User.objects.get(id=request.session['user_id'])
                if update_this == user:
                    print('updating atm')
                    update_this.first_name=request.POST['first_name']
                    update_this.last_name=request.POST['last_name']
                    update_this.email=request.POST['email']
                    update_this.save()
        return redirect('/quotes')

def delete(request, id):
    if request.method == 'POST':
        delete_this = Quote.objects.filter(id = id)
        if delete_this:
            delete_this_quote = delete_this[0]
            user = User.objects.get(id=request.session['user_id'])
            if delete_this_quote.posted_by == user:
                delete_this_quote.delete()
        return redirect('/quotes')

def like(request,id):
    if request.method == 'POST':
        quoteLike = Quote.objects.filter(id=id)
        if quoteLike:
            quote = quoteLike[0]
            user = User.objects.get(id=request.session['user_id'])
            quote.user_likes.add(user)
    return redirect('/quotes')
