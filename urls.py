from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("temp", views.temp, name="temp"),
    path('save_image', views.save_image, name="save_image"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/', include('allauth.urls')),
]