# conteudos_tcc/admin.py
from django.contrib import admin
from .models import Capitulo, Secao ,Recurso# Importe seus modelos

@admin.register(Capitulo)
class CapituloAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ordem', 'data_criacao', 'data_atualizacao')
    prepopulated_fields = {'slug': ('titulo',)} # O slug é preenchido automaticamente ao digitar o título
    search_fields = ('titulo', 'resumo')
    list_filter = ('data_criacao', 'data_atualizacao')
    # Adicione 'imagem_capa' ao fields para que apareça no formulário de edição do admin
    fields = ('titulo', 'slug', 'ordem', 'resumo', 'imagem_capa')


@admin.register(Secao)
class SecaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'capitulo', 'ordem', 'data_criacao', 'data_atualizacao')
    prepopulated_fields = {'slug': ('titulo',)}
    list_filter = ('capitulo', 'data_criacao', 'data_atualizacao')
    search_fields = ('titulo', 'conteudo_html')
    raw_id_fields = ('capitulo',) # Facilita a seleção do capítulo em grande número
    # Adicione 'conteudo_html' e 'imagem_ilustrativa' ao fields
    fields = ('capitulo', 'titulo', 'slug', 'ordem', 'conteudo_html', 'imagem_ilustrativa')


@admin.register(Recurso)
class RecursoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'ordem', 'data_criacao')
    list_filter = ('tipo',)
    search_fields = ('titulo', 'descricao')
    # Use fieldsets para organizar os campos no admin, mostrando/escondendo arquivo/url
    fieldsets = (
        (None, {
            'fields': ('titulo', 'descricao', 'tipo', 'ordem')
        }),
        ('Conteúdo do Recurso', {
            'fields': ('arquivo', 'url'),
            'description': 'Preencha apenas o campo relevante para o tipo de recurso selecionado.'
        }),
    )

    # Adiciona JavaScript para mostrar/esconder campos baseado no tipo
    class Media:
        js = (
            'admin/js/jquery.init.js', # Garante que o jQuery do Django esteja disponível
            'conteudos_tcc/js/recurso_admin.js', # Seu script personalizado
        )