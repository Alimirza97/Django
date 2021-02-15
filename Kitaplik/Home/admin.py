from django.contrib import admin
from .models import Language
from .models import CapType
from .models import Publisher
from .models import Author
from .models import Book
from .models import Category
from .models import Users

# Register your models here.
admin.site.register(Language)
admin.site.register(CapType)
admin.site.register(Publisher)
admin.site.register(Category)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname")


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ("name", "author", "publisher")

@admin.register(Users)
class UseraAdmin(admin.ModelAdmin):
    list_display = ("firstname", "lastname", "age", "Speed")

    def Speed(self, obj):
        return "Günde " + str(obj.speed) + " Sayfa"

    Speed.short_description = "Okuma Hızı"
