from django.contrib import admin
from django.urls import path, include
from apisumple import views

urlpatterns = [
    path('', include('apisumple.urls')),
    path('admin/', admin.site.urls),
]
