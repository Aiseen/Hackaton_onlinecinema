from rest_framework.routers import DefaultRouter

from apps.towatch.views import ContactView

router =  DefaultRouter()
router.register('', ContactView)


urlpatterns = []
urlpatterns.extend(router.urls)