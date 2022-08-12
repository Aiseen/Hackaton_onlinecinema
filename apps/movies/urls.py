from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from apps.movies.models import Image
from apps.movies.views import CategoryView, FilmView, ReviewView

router = DefaultRouter()
router.register('category', CategoryView)
router.register('review', ReviewView)
router.register('',FilmView)


class ImageInAdmin(admin.TabularInline):
    model = Image
    fields = ['image']
    max_num = 5


urlpatterns = [
    path('', include(router.urls))
]