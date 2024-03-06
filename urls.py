from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("u/<str:username>", views.graffiti, name="graffiti"),
    path('accounts/profile/', views.saveTwitterBanner, name='saveTwitterBanner'),
    path('share', views.share, name="share"),
    path('accounts/', include('allauth.urls')),
    path('save_image/<str:username>', views.save_image, name="save_image"),
]