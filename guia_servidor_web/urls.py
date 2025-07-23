# guia_servidor_web/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings # <--- IMPORTANTE: Importe settings
from django.conf.urls.static import static # <--- IMPORTANTE: Importe static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('conteudos_tcc.urls')),
]

# ESTAS LINHAS SÃO CRUCIAIS PARA SERVIR STATICOS E MIDIA EM AMBIENTE DE DESENVOLVIMENTO
# ELAS SÓ FUNCIONAM QUANDO DEBUG = TRUE
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)