from django.contrib import admin
from django.urls import path, include
from api import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('contact/', views.contact, name='contact'),
    path('', include('api.urls')),
]
