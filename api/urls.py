from django.urls import path
from . import views

urlpatterns = [
    path('', views.about),
    path('about/', views.about),
    path('contact/', views.contact, name='contact'),
    path('chat/', views.chat, name='chat'),

]