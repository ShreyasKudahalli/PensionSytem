from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('apply-pension/', views.apply_pension, name='apply_pension'),
    path('status/', views.pension_status, name='pension_status'),
]