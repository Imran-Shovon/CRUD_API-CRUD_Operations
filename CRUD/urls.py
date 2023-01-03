from django.contrib import admin
from django.urls import include, path

app_name = "api"
urlpatterns = [
    path("admin/", admin.site.urls),
    path('', include("api.urls")),
]
