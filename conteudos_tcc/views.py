# conteudos_tcc/views.py

from django.shortcuts import render, get_object_or_404
from .models import Capitulo, Secao, Recurso # Importe o novo modelo

def home_page(request):
    # ... (código existente da home_page) ...
    capitulos = Capitulo.objects.all().order_by('ordem')
    todos_capitulos = Capitulo.objects.all().order_by('ordem')
    context = {
        'capitulos': capitulos,
        'todos_capitulos': todos_capitulos,
    }
    return render(request, 'conteudos_tcc/home.html', context)

def detalhe_capitulo(request, capitulo_slug):
    # ... (código existente da detalhe_capitulo) ...
    capitulo = get_object_or_404(Capitulo, slug=capitulo_slug)
    secoes = capitulo.secoes.all().order_by('ordem')
    todos_capitulos = Capitulo.objects.all().order_by('ordem')
    context = {
        'capitulo': capitulo,
        'secoes': secoes,
        'todos_capitulos': todos_capitulos,
    }
    return render(request, 'conteudos_tcc/detalhe_capitulo.html', context)

# NOVA VIEW: recursos_page
def recursos_page(request):
    """
    Função para exibir a página de recursos (downloads e links sugeridos).
    """
    recursos = Recurso.objects.all().order_by('ordem')
    downloads = recursos.filter(tipo=Recurso.TipoRecurso.DOWNLOAD)
    links = recursos.filter(tipo=Recurso.TipoRecurso.LINK)

    todos_capitulos = Capitulo.objects.all().order_by('ordem') # Para a navbar

    context = {
        'downloads': downloads,
        'links': links,
        'todos_capitulos': todos_capitulos,
    }
    return render(request, 'conteudos_tcc/recursos.html', context)