from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view


schema_view = get_schema_view(
    openapi.Info(
        title='КИНО ОТ АЙСЕНА',
        default_version='v1',
        description='Бесплатный просмотр фильмов в HD'
    ),
    public=True
)



urlpatterns = [
    path('admin/', admin.site.urls),
    path('swagger/', schema_view.with_ui('swagger')),
    path('api/v1/account/', include('apps.account.urls')),
    path('api/v1/movies/', include('apps.movies.urls'))
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)