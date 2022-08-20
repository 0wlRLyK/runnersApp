"""runnersApp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="Runners app API",
      default_version='v0.1',
      description="""
      <h2>API documentation for running app</h2> <hr>
      <i>Author of idea and main front-end developer:</i>
      <strong><a href='https://github.com/julgrabar/Langui'>julgrabar</a></strong>
      <i>API author and back-end developer:</i>
      <strong><a href='https://github.com/0wlRLyK'>0wlRLyK</a></strong><br>
      <h3>Schema:</h3>
      <ul>
      <li>Week</li>
          <ul>
          <li>Training</li>
                <ul>
                  <li>Exercise</li>
                </ul>
          </ul>

      </ul>
      """,
      contact=openapi.Contact(email="denys.nedzvetskyi@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api = [
    path("", include("app.urls")),
    path("users/", include("users.urls")),
]
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(api)),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
