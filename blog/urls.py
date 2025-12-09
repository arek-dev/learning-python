# blog/urls.py
from django.urls import path

from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='home'),  # Landing page
    path('lekcje/', views.lesson_list, name='lesson_list'),  # Lista lekcji
    path('lekcje/<slug:category_slug>/', views.lesson_list, name='lesson_list_by_category'),  # Filtr kategorii
    path('lekcja/<slug:slug>/', views.lesson_detail, name='lesson_detail'),  # Szczegóły lekcji
    path('o-mnie/', views.about, name='about'),  # Strona o mnie
    path('biblioteka/', views.resources, name='resources'),  # Biblioteka zasobów
]
