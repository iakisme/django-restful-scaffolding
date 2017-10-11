from django.conf.urls import url, include
from rest_framework_bulk.routes import BulkRouter


from .views import ContentTypeViewSet

router = BulkRouter()
router.register('contenttypes', ContentTypeViewSet)

urlpatterns = (
    url(r'^', include(router.urls)),
)