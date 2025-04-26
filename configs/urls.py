from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from api.v1.routers import urlpatterns as v1_api_routers

from django.conf import settings
from django.conf.urls.static import static  # 👈 این مهمه

schema_view = get_schema_view(
   openapi.Info(
      title="Metallurgical Researcher Center Title",
      default_version='v1',
      description="api docs for Metallurgical Researcher Center\n base url : api/v1/ \n GraphQL link : http://127.0.0.1:8000/api/v1/graphql/blogs",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="rezabhm50@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-docs/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api-docs/re-doc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/v1/', include(v1_api_routers)),
]

# 👇 این خط حتماً بعد از urlpatterns قرار بگیره
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)