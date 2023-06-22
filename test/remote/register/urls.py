from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

app_name = 'register'


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('forgotpassword/', views.forgot_password, name='forgotpassword'),
    #path('password_reset/', views.password_reset_view, name='password_reset'),
    path('password_reset_success/', views.password_reset_success, name='password_reset_success'),
    path('myprofile/', views.myprofile, name='myprofile'),
    path('register/success/', views.register_success, name='register_success'),
    path('viewusers/', views.viewusers, name='viewusers'),
    path('test/', views.send_email, name='test'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





