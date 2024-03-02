from django.urls import path, include

from . import views

urlpatterns = [
    path("u/<str:username>", views.graffiti, name="graffiti"),
    path("temp", views.temp, name="temp"),
    path('save_image/<str:username>', views.save_image, name="save_image"),
    path("update/", views.update, name="update"),
    path('accounts/profile/', views.profile_view, name='profile'),
    path('accounts/', include('allauth.urls')),
]