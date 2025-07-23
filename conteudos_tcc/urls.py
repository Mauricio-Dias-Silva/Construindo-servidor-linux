# conteudos_tcc/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('recursos/', views.recursos_page, name='recursos_page'), # <-- AGORA ANTES DO SLUG!
    path('<slug:capitulo_slug>/', views.detalhe_capitulo, name='detalhe_capitulo'),
]