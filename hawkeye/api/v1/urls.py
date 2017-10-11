from django.conf.urls import url, include
from .auth import urls as auth_urls
from .misc import urls as misc_urls

urlpatterns = [
    url(r'^auth/', include(auth_urls, namespace='auth')),
    url(r'^misc/', include(misc_urls, namespace='misc')),
]
