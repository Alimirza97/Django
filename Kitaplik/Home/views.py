from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *

import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def get_important_features(data):
    important_features = []
    for i in range(0, data.shape[0]):
        important_features.append(data['Yazar'][i] + ' ' + data['Kategori'][i])
    return important_features

def FindBook(book_name):
    books_id = []
    j = 0
    try:
        # Store the data
        df = pd.read_csv('books_data.csv', error_bad_lines=False)
        # Creat a list of important colomns for the recommendation engine
        # colomns = ['Adi', 'Yazar', 'Yayinevi','Kategori','Dil']
        colomns = ['Yazar', 'Kategori']

        # Create a colomn to hold the combined satrings
        df['important_features'] = get_important_features(df)

        # Convert the text to a matrix of token counts
        cm = CountVectorizer().fit_transform(df['important_features'])

        # Get the cosine similarity matrix from the count matrix
        cs = cosine_similarity(cm)

        # Find the book id
        _book_id = df[df.Adi == str(book_name)]['ID'].values[0]

        # Creat a list of enumerations for the similarity score [ ( book_id, similarity score ), (...) ]
        scores = list(enumerate(cs[_book_id]))

        # Sort the list
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)
        sorted_scores = sorted_scores[1:]

        # Creat a loop to print the first 7 similar books
        print(str(book_name) + ' için önerdiğimiz 7 kitap daha:')
        for item in sorted_scores:
            book_title = df[df.ID == item[0]]['ID'].values[0]

            books_id.append(book_title)
            j = j + 1
            if j == 7:
                break
    except:
        book_id = []

    return books_id

def index(request):
    books = []
    my_user = []
    if request.user.is_authenticated:
        userss = list(Users.objects.all())
        my_user = None
        for users in userss:
            if users.user == request.user:
                my_user = users
        if my_user is None:
            books = list(Book.objects.all())[-4:]
        else:
            books = list(my_user.books.all())
        if not books:
            books = list(Book.objects.all())[-4:]
    else:
        books = list(Book.objects.all())[-4:]
    all_books = len(list(Book.objects.all()))
    best_books = list(Book.objects.all())[:4]
    publishers = len(list(Publisher.objects.all()))
    users = len(list(Users.objects.all()))
    author = len(list(Author.objects.all()))
    return render(request, 'Home/index.html', {
        'title': 'Ana Sayfa', 'books': books, 'best_books': best_books,
        'all_books': all_books, 'publishers': publishers, 'users': users,
        'author': author, 'my_user': my_user
    })


def about(request):
    books = list(Book.objects.all())[-3:]
    return render(request, 'Home/about.html',{'title': 'Hakkımızda', 'books': books})

def contact(request):
    return render(request, 'Home/contact.html',{'title': 'Benim Sayfam'})

def content(request):
    books_list = Book.objects.order_by('name')
    query = request.GET.get('search')
    if query:
        books_list = books_list.filter(name__icontains=query)
    paginator = Paginator(books_list, 10)  # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Home/content.html',{'title' : 'İçerik', 'books': page_obj})

@login_required(login_url='login')
def my_page(request):
    userss = list(Users.objects.all())
    my_user = None
    for users in userss:
        if users.user == request.user:
            my_user = users
    if my_user is None:
        return render(request, 'registration/login.html', {'title': 'Giriş Yap'})
    books = list(my_user.books.all())
    recommendation_books = []
    for book in books:
        find_books = FindBook(book)
        for book_id in find_books:
            my_book = Book.objects.get(id = book_id)
            recommendation_books.append(my_book)
    recommendation_books = list(set(recommendation_books))

    paginator = Paginator(recommendation_books, 10)  # Show 10 books per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'Home/my_page.html',{'title' : 'Benim Sayfam', 'my_user': my_user, 'books': page_obj})

@login_required(login_url='login')
def profil(request):
    books = len(list(Book.objects.all()))
    password_form = ChangePasswordForm(request.user)
    userss = list(Users.objects.all())
    my_user = None
    for users in userss:
        if users.user == request.user:
            my_user = users
    if my_user is None:
        return render(request, 'registration/login.html', {'title': 'Giriş Yap'})
    user_form = CreatUserForm(initial={'email': request.user.email})
    profil_form = ProfileUserForm(initial={
        'firstname': my_user.firstname,
        'lastname': my_user.lastname,
        'phone': my_user.phone,
        'mobile': my_user.mobile,
        'dateOfBirth': my_user.dateOfBirth,
        'placeOfBirth': my_user.placeOfBirth,
        'age': my_user.age,
        'speed': my_user.speed,
        'profilPhoto': my_user.profilPhoto,
        'language': my_user.language.all()
    })
    add_book = AddBookToProfil(initial={'books': my_user.books.all(), 'reading_book': my_user.reading_book})
    reading_book_count = len(list(my_user.books.all()))
    if my_user.reading_book:
        reading_book_page_count = Book.objects.get(name = my_user.reading_book.name).pageCount
    else:
        reading_book_page_count = 0
    if request.method == 'POST':
        if request.POST.get('password_save') == 'sifre_kaydet':
            if request.user.is_authenticated:
                password_form = ChangePasswordForm(request.user, request.POST)
                if password_form.is_valid():
                    user = password_form.save()
                    update_session_auth_hash(request, user)  # Important!
                    messages.success(request, 'Şifreniz Başarılı Bir Şekilde Değiştirildi')
                    return redirect('profil')
                else:
                    messages.error(request, 'Şifre Hatalı Girilmiştir.')
            else:
                return redirect('login')

        elif request.POST.get('profil_save') == 'profil_kaydet':
            profil_form = ProfileUserForm(request.POST)
            if request.user.is_authenticated:
                if profil_form.is_valid():
                    for users in userss:
                        if users.user == request.user:
                            users.firstname = profil_form.cleaned_data.get('firstname')
                            users.lastname = profil_form.cleaned_data.get('lastname')
                            users.phone = profil_form.cleaned_data.get('phone')
                            users.mobile = profil_form.cleaned_data.get('mobile')
                            users.dateOfBirth = profil_form.cleaned_data.get('dateOfBirth')
                            users.profilPhoto = profil_form.cleaned_data.get('profilPhoto')
                            users.placeOfBirth = profil_form.cleaned_data.get('placeOfBirth')
                            users.age = profil_form.cleaned_data.get('age')
                            users.speed = profil_form.cleaned_data.get('speed')
                            users.language.set(profil_form.cleaned_data.get('language'))
                            users.save()
                    return redirect('profil')
                else:
                    messages.warning(request, 'Profil Sayfasındaki Eksik Bilgileri Doldurunuz.')
            else:
                return redirect('login')

        elif request.POST.get('book_save') == 'kitap_kaydet':
            add_book = AddBookToProfil(request.POST)
            if request.user.is_authenticated:
                if add_book.is_valid():
                    for users in userss:
                        if users.user == request.user:
                            users.books.set(add_book.cleaned_data.get('books'))
                            users.reading_book = add_book.cleaned_data.get('reading_book')
                            users.save()
                    return redirect('profil')
                else:
                    messages.warning(request, 'Kitap Sayfasındaki Eksik Bilgileri Doldurunuz.')
            else:
                return redirect('login')
    return render(request, 'Home/profil.html',{
        'title' : 'Profil', 'password_form' : password_form,
        'user_form' : user_form, 'profil_form' : profil_form,
        'book_form' : add_book, 'my_user' : my_user,
        'books' : books, 'reading_book_count': reading_book_count,
        'remaining_books': books-reading_book_count,
        'remaining_time': round(reading_book_page_count / my_user.speed)
    })

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            dj_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Kullanıcı adı veya şifre hatalı')
    return render(request, 'registration/login.html',{'title' : 'Giriş Yap'})

def logout(request):
    dj_logout(request)
    return redirect('home')

def register(request):
    """return redirect('home')"""

    user_form = CreatUserForm()
    profil_form = ProfileForm()
    if request.method == 'POST':
        profil_form = ProfileForm(request.POST)
        user_form = CreatUserForm(request.POST)
        if user_form.is_valid() and profil_form.is_valid():
            user = user_form.save()
            profil_form = profil_form.save(commit=False)
            profil_form.user = user
            profil_form.save()
            username = user_form.cleaned_data.get('username')
            messages.success(request, 'Merhaba ' + username + ' ailemize hoşgeldiniz. Kullanıcı adı ve şifrenizle giriş yapabilirsiniz')
            return redirect('login')

    return render(request, 'registration/register.html', {'title' : 'Kayıt Ol', 'user_form': user_form, 'profil_form': profil_form})