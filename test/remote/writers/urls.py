from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views
app_name = 'writers'

urlpatterns = [
    path('dashboard/', login_required(views.writersdashboard), name='dashboard'),
]

