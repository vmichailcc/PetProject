from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from store.urls import store_router, comment_router, like_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("store.urls")),
    path('', include("accounts.urls")),
    path('api/store/', include(store_router.urls)),
    path('api/comment/', include(comment_router.urls)),
    path('api/like/', include(like_router.urls)),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
