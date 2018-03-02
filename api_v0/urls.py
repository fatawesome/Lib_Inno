from rest_framework.routers import DefaultRouter
from .views import *


router = DefaultRouter()
router.register(r'books', BookViewSet)
router.register(r'articles', ArticleViewSet)


urlpatterns = router.urls
