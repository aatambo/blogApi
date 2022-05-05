from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import HomeView

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("admin/", admin.site.urls),
    path("api/v1/", include("users.urls", namespace="users")),
    path("api/v1/", include("blog.urls", namespace="blog")),
    path("", include("swagger.urls", namespace="swagger")),
    path("o/", include("oauth2_provider.urls", namespace="oauth2_provider")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
