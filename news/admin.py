from django.contrib import admin

from .models import Category, Comment, News


class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "name", "slug")
    search_fields = ("name",)
    empty_value_display = "-пусто-"


class NewsAdmin(admin.ModelAdmin):
    list_display = ("pk", "heading", "text", "category", "pub_date", "image")
    search_fields = ("heading", "text")
    empty_value_display = "-пусто-"


class NewsAdminComment(admin.ModelAdmin):
    list_display = ("pk", "author", "news", "text", "pub_date", "parent")
    search_fields = ("news", "author", "text")
    list_filter = ("author", "pub_date")


admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Comment, NewsAdminComment)
