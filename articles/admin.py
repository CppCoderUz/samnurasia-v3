from django.contrib import admin


from .models import (
    Article,
    ArticleColumn,
    Journal,
    Petition,
    Post
)

@admin.register(Journal)
class JournalAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']


@admin.register(ArticleColumn)
class ArticleColumnAdmin(admin.ModelAdmin):
    list_display = ['name', 'pk']


@admin.register(Petition)
class PetitionAdmin(admin.ModelAdmin):
    list_display = ['title', 'date_time', 'status', 'is_viewed', 'confirmed', 'first_name', 'last_name', 'email']

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'approved_date_time',
        'journal', 'column',
        'confirmed', 'first_name',
        'last_name'
    ]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'date_time', 'image']