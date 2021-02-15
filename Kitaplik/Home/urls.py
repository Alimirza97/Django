from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.index, name = 'home'),
    path('about', views.about, name = 'about'),
    path('contact', views.contact, name = 'contact'),
    path('content', views.content, name = 'content'),
    path('my_page', views.my_page, name='my_page'),
    path('profil', views.profil, name='profil'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('register', views.register, name = 'register'),
]
