from django.db import models
from django.contrib.auth.models import User

class Language(models.Model):
    name = models.CharField('Dil Adı', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Dil'
        verbose_name_plural = 'Diller'

class Publisher(models.Model):
    name = models.CharField('Yayınevi Adı', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Yayınevi'
        verbose_name_plural = 'Yayınevleri'

class Author(models.Model):
    firstname = models.CharField('Adı', max_length=50)
    lastname = models.CharField('Soyadı', max_length=50)
    dateOfBirth = models.DateField('Doğum Tarihi', null=True, blank=True)
    placeOfBirth = models.TextField('Doğum Yeri', null=True, blank=True)

    def __str__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        verbose_name = 'Yazar'
        verbose_name_plural = 'Yazarlar'
        ordering = ("firstname", "lastname")

class Category(models.Model):
    name = models.CharField('Kategori Adı', max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kategori'
        verbose_name_plural = 'Kategoriler'

class CapType(models.Model):
    name = models.CharField('Kapak Türü', max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kapat Türü'
        verbose_name_plural = 'Kapak Türleri'

class Book(models.Model):
    name = models.CharField('Kitap Adı', max_length=100)
    pageCount = models.IntegerField('Sayfa Sayısı')
    point = models.CharField('Puan', max_length=10)
    language = models.ForeignKey(Language, verbose_name='Dil', on_delete=models.CASCADE)
    coverPhoto = models.ImageField('Kapak Fotoğrafı')
    description = models.TextField('Açıklama', null=True, blank=True)
    publisher = models.ForeignKey(Publisher, verbose_name='Yayınevi', on_delete=models.CASCADE)
    author = models.ForeignKey(Author, verbose_name='Yazar', on_delete=models.CASCADE)
    capType = models.ForeignKey(CapType, verbose_name='Kapak Türü', on_delete=models.CASCADE)
    bookCategory = models.ManyToManyField(Category, verbose_name='Kategori')


    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Kitap'
        verbose_name_plural = 'Kitaplar'
        ordering = ("name", "author", "publisher")


class Users(models.Model):
    user = models.OneToOneField(User, verbose_name='User', on_delete=models.CASCADE)
    firstname = models.CharField('Adı', max_length=50)
    lastname = models.CharField('Soyadı', max_length=50)
    phone = models.CharField('Telefon', max_length=20, null=True, blank=True)
    mobile = models.CharField('Telefon', max_length=20, null=True, blank=True)
    dateOfBirth = models.DateField('Doğum Tarihi', null=True, blank=True)
    placeOfBirth = models.TextField('Doğum Yeri', null=True, blank=True)
    age = models.IntegerField("Yaşı", null=True, blank=True)
    speed = models.IntegerField("Okuma Hızı(Günlük)", null=True, blank=True, default='1')
    profilPhoto = models.ImageField('Profil Fotoğrafı', null=True, blank=True)
    language = models.ManyToManyField(Language, verbose_name='Dil', null=True, blank=True)
    books = models.ManyToManyField(Book, verbose_name='Kitaplar', null=True, blank=True)
    reading_book = models.OneToOneField(Book, verbose_name='Şuan Okuduğu Kitap', on_delete=models.DO_NOTHING, related_name='book_reading_book', null=True, blank=True)
    reading_book_addition_date = models.DateField(verbose_name='Okuduğu Kitabı Ekleme Tarihi', null=True, blank=True)


    def __str__(self):
        return self.firstname + " " + self.lastname

    class Meta:
        verbose_name = 'Kullanıcı'
        verbose_name_plural = 'Kullanıcılar'
        ordering = ("firstname", "lastname", "age", "speed")


