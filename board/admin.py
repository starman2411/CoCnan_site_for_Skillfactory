from django.contrib import admin
from .models import Post, Category, PostCategory


class PostCategoryInline(admin.TabularInline):
    model = PostCategory
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostCategoryInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Category)
