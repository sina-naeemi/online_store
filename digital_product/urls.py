
from django.contrib import admin
from django.urls import path , include

from django.conf import settings
from django.conf.urls.static import static

from django.conf.urls import include

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView , SpectacularRedocView


urlpatterns = [
    path('admin/', admin.site.urls),
    path("" , include("products.urls")),
    path("" , include("User.urls")),
    path("" , include("peyments.urls")),
    path("",include("subscriptions.urls")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path("redoc/",SpectacularRedocView.as_view(url_name="schema"),name="redoc"),
]

if settings.IS_DEVEL==True :
    urlpatterns+= static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
