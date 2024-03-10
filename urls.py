from django.urls import path, include

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('login', views.login, name="login"),
    path('demo', views.demo, name="demo"),
    path("u/<str:username>", views.graffiti, name="graffiti"),
    path('accounts/profile/', views.saveTwitterBanner, name='saveTwitterBanner'),
    path("upload/<str:username>", views.upload, name="upload"),
    path('share', views.share, name="share"),
    path('accounts/', include('allauth.urls')),
    path('save_image/<str:username>', views.save_image, name="save_image"),
]