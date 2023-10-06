from django.contrib import admin
from .models import Post, Category


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'category', 'timePost', 'title')


# admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
# Register your models here.
