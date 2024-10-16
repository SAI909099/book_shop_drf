from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from root import settings

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('apps.urls')),
                  path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
                  # Optional UI:
                  path('', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

                  # path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
                  # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                                         document_root=settings.STATIC_ROOT)
