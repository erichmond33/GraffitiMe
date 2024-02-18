from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("temp", views.temp, name="temp"),
    path('save_image', views.save_image, name="save_image"),
]