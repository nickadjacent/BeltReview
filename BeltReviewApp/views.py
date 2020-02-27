from django.shortcuts import render, redirect

from django.contrib import messages

from .models import *

import bcrypt


# ********** functions that render page **********

def index(request):
    print('rendering login/reg page')
    return render(request, 'index.html')


def user_dashboard(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')
    context = {
        'user': User.objects.get(email=request.session['email_session_id'])
    }
    print('rendering user_dashboard page')
    return render(request, 'user_dashboard.html', context)


def add_book(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    print('rendering add_book page')
    return render(request, 'add_book.html')


def book_info(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    print('rendering add_review page')
    return render(request, 'book_info.html')


def user_page(request):
    # only allow user into dashboard if they have session id
    if request.session.get('email_session_id') == None:
        print('no session in email_session_id')
        return redirect('/')

    print('rendering user_page page')
    return render(request, 'user_page.html')


# ***** functions that redirect to render page *****

def register(request):
    # print('registering new user')
    # return redirect('/user_dashboard')

    print(request.POST)
    print('registering a new user')

    # check first for validations (password match, etc...)
    errors = User.objects.basic_validations(request.POST)
    # check if the errors dictionary has antyhingin it
    if len(errors) > 0:
        # if erros dictionary contains anything, loop through each key-value pair and make a flash message.
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')

    # code some stuff to register a user in DB
    # before creating a user, check for uniqueness
    # check DB for the email
    user_in_db = User.objects.filter(email=request.POST['email'])
    if len(user_in_db) > 0:
        print('Email already exists')
        messages.error(request, "There was a problem.")
        return redirect('/')
    else:
        hashed_pw = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print('hashed_pw:', hashed_pw)
        user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            alias=request.POST['alias'],
            email=request.POST['email'],
            password=hashed_pw,
        )
        # add new user to session
        request.session['email_session_id'] = user.email
        return redirect('/user_dashboard')


def login(request):
    print(request.POST)
    print('logging in a user')

    # check to see if email exists in DB
    user = User.objects.filter(email=request.POST['email'])
    if len(user) == 1:
        print('user found -> logging user in')
        if bcrypt.checkpw(request.POST['password'].encode(), user[0].password.encode()):
            print("password match")
            # start a session when a user logs in
            print('creating email_session_id for user')
            request.session['email_session_id'] = user[0].email
            return redirect('/user_dashboard')
        else:
            print("failed password")
            messages.error(request, "There was an error.")
        return redirect('/')
    else:
        print('no user found')
        messages.error(request, "There was an error.")
        return redirect('/')


def logout(request):
    print('loggin out user')
    print('clearing session email_session_id')
    request.session.clear()
    return redirect('/')


def book_page(request):
    print('redirecting to book_info')
    return redirect('/book_info')


def create_new_book(request):
    print('creating a new book in DB')
    print(request.POST)

    book_in_db = Book.objects.filter(title=request.POST['title'])
    if len(book_in_db) > 0:
        print('Book title already exists')
        messages.error(request, "Book title already exists.")
        return redirect('/add_book')

    else:
        author_list = Author.objects.filter(name=request.POST['author'])

        if len(author_list) == 0:
            new_author = Author.objects.create(
                name=request.POST['author']
            )
        else:
            new_author = author_list[0]

        new_book = Book.objects.create(
            title=request.POST['title'],
            author=request.POST['author'],
            user_review=request.POST['review']
        )
        messages.success(request, 'Book successfully created')

        return redirect(f'/book_info/{new_book.id}')
