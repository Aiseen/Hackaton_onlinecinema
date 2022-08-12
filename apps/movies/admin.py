from django.contrib import admin

from apps.movies.models import Category, Film, Image, Like, Review, Rating, Favourite

admin.site.register(Category)
admin.site.register(Image)
admin.site.register(Like)
admin.site.register(Review)
admin.site.register(Rating)
admin.site.register(Favourite)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5


class FilmAdmin(admin.ModelAdmin):
    list_display = ['name','category']
    search_fields = ['name']


admin.site.register(Film,FilmAdmin)