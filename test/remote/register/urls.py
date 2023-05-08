from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('register/success/', views.register_success, name='register_success'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

