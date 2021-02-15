from django.forms import ModelForm, DateInput, TextInput, Textarea, EmailInput, PasswordInput, SelectMultiple, Select
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from .models import Users
from django import forms

class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super(ChangePasswordForm, self).__init__(user, *args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'name': 'old_password',
            'placeholder': 'Eski Şifre..',
            'title': 'Eski Şifrenizi Girin.'
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'name': 'new_password1',
            'placeholder': 'Yeni Şifre..',
            'title': 'Yeni Şifrenizi Girin.'
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'name': 'new_password2',
            'placeholder': 'Yeni Şifre Tekrar..',
            'title': 'Yeni Şifrenizi Tekrar Girin.'
        })


class CreatUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={
                'class': 'form-control',
                'name': 'username',
                'placeholder': 'Kullanıcı Adı..',
                'title': 'Kullanıcı Adınızı Girin..',
            }),
            'email': EmailInput(attrs={
                'class': 'form-control',
                'name': 'email',
                'placeholder': 'Email..',
                'title': 'Email Adresinizi Girin.',
            }),
            'password1': PasswordInput(attrs={
                'class': 'form-control',
                'name': 'password1',
                'placeholder': 'Şifre..',
                'title': 'Şifrenizi Girin.',
            }),
            'password2': PasswordInput(attrs={
                'class': 'form-control',
                'name': 'password2',
                'placeholder': 'Şifre Tekrar..',
                'title': 'Şifrenizi Tekrar Giriniz.',
            })
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['firstname', 'lastname']
        widgets = {
            'firstname': TextInput(attrs={
                'class': 'form-control',
                'name': 'firstname',
                'placeholder': 'Ad..',
                'title': 'Adınızı Girin..',
            }),
            'lastname': TextInput(attrs={
                'class': 'form-control',
                'name': 'lastname',
                'placeholder': 'Soyad..',
                'title': 'Soyadınızı Girin.',
            })
        }

class ProfileUserForm(forms.ModelForm):

    class Meta:
        model = Users
        fields = ['firstname', 'lastname', 'phone', 'mobile', 'dateOfBirth', 'placeOfBirth', 'age', 'speed', 'profilPhoto', 'language']
        widgets = {
            'firstname': TextInput(attrs={
                'class': 'form-control',
                'name': 'first_name',
                'placeholder': 'Ad..',
                'title': 'Adınızı Girin',
            }),
            'lastname': TextInput(attrs={
                'class': 'form-control',
                'name': 'last_name',
                'placeholder': 'Soyadınızı Girin..',
                'title': 'Soyadınızı Girin',
            }),
            'phone': TextInput(attrs={
                'class': 'form-control',
                'name': 'phone',
                'placeholder': 'Ev Telefonu..',
                'title': 'Eğer Varsa Ev Telefonunuzu Girin.',
            }),
            'mobile': TextInput(attrs={
                'class': 'form-control',
                'name': 'mobile',
                'placeholder': 'Cep Telefonu..',
                'title': 'Eğer Varsa Cep Telefonunuzu Girin.',
            }),
            'dateOfBirth': DateInput(attrs={
                'type': 'date',
                'class': 'form-control',
                'name': 'dateOfBirth',
                'placeholder': 'Doğum Tarihi..',
                'title': 'Doğum Tarihinizi Girin.',
            }),
            'placeOfBirth': Textarea(attrs={
                'class': 'form-control',
                'name': 'placeOfBirth',
                'placeholder': 'Doğum Yeri..',
                'title': 'Doğum Yerinizi Girin.',
            }),
            'age': TextInput(attrs={
                'class': 'form-control',
                'name': 'age',
                'placeholder': 'Yaşınız..',
                'title': 'Yaşınızı Girin.',
            }),
            'speed': TextInput(attrs={
                'class': 'form-control',
                'name': 'speed',
                'placeholder': 'Günlük Okunan Sayfa Sayısı..',
                'title': 'Bir Gün İçinde Okuduğunuz Sayfa Sayısını Giriniz.',
            }),
            'language': SelectMultiple(attrs={
                'class': 'form-control',
                'name': 'language',
                'placeholder': 'Dil..',
                'title': 'Dil Tercihinizi Girin.',
            })
        }

class AddBookToProfil(forms.ModelForm):
    class Meta:
        model = Users
        fields = ['books', 'reading_book']
        widgets = {
            'books': SelectMultiple(attrs={
                'class': 'form-control',
                'name': 'books',
                'placeholder': 'Kitaplar..',
                'title': 'Okuduğunuz Kitapları Seçiniz.',
                'size': '25'
            }),
            'reading_book': Select(attrs={
                'class': 'form-control',
                'name': 'reading_book',
                'placeholder': 'Dil..',
                'title': 'Şuanda Okuduğunuz Kitabı Seçin.',
                'size' : '25'
            })
        }