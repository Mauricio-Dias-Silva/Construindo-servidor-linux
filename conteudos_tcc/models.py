# conteudos_tcc/models.py
from django.db import models
from django.utils.text import slugify # Para gerar slugs automaticamente
from django.utils.translation import gettext_lazy as _

class Capitulo(models.Model):
    titulo = models.CharField(max_length=200, help_text="Título principal do capítulo.")
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                            help_text="URL amigável do capítulo (gerado automaticamente).")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição do capítulo.")
    resumo = models.TextField(blank=True, help_text="Um breve resumo do capítulo.")
    # Adicione esta linha para a imagem de capa do capítulo
    imagem_capa = models.ImageField(upload_to='capitulo_capas/', blank=True, null=True, help_text="Imagem de capa para o capítulo.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['ordem', 'titulo'] # Define a ordem padrão dos capítulos
        verbose_name = "Capítulo"
        verbose_name_plural = "Capítulos"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Capítulo {self.ordem}: {self.titulo}"

class Secao(models.Model):
    capitulo = models.ForeignKey(Capitulo, on_delete=models.CASCADE, related_name='secoes',
                                 help_text="Capítulo ao qual esta seção pertence.")
    titulo = models.CharField(max_length=200, help_text="Título da seção.")
    slug = models.SlugField(max_length=200, unique=True, blank=True,
                            help_text="URL amigável da seção (gerado automaticamente).")
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição da seção dentro do capítulo.")
    conteudo_html = models.TextField(blank=True, help_text="Conteúdo HTML da seção. Use tags HTML aqui.")
    imagem_ilustrativa = models.ImageField(upload_to='secao_imagens/', blank=True, null=True, help_text="Imagem para ilustrar a seção.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['capitulo__ordem', 'ordem', 'titulo'] # Ordem padrão das seções
        unique_together = ('capitulo', 'slug') # Garante slug único por capítulo
        verbose_name = "Seção"
        verbose_name_plural = "Seções"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.capitulo.ordem}.{self.ordem}: {self.titulo}"
    


class Recurso(models.Model):
    class TipoRecurso(models.TextChoices):
        DOWNLOAD = 'DOWNLOAD', _('Download')
        LINK = 'LINK', _('Link Externo')

    titulo = models.CharField(max_length=200, help_text="Título do recurso (ex: 'Script de Instalação Nginx', 'Documentação Django').")
    descricao = models.TextField(blank=True, help_text="Uma breve descrição do recurso.")
    tipo = models.CharField(
        max_length=10,
        choices=TipoRecurso.choices,
        default=TipoRecurso.LINK,
        help_text="Selecione o tipo de recurso: Download de arquivo ou Link externo."
    )
    arquivo = models.FileField(upload_to='recursos_downloads/', blank=True, null=True,
                               help_text="Para recursos do tipo 'Download', faça upload do arquivo aqui.")
    url = models.URLField(blank=True, null=True,
                          help_text="Para recursos do tipo 'Link Externo', insira a URL aqui.")
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ordem = models.IntegerField(default=0, help_text="Ordem de exibição do recurso.")

    class Meta:
        ordering = ['ordem', 'titulo']
        verbose_name = "Recurso Adicional"
        verbose_name_plural = "Recursos Adicionais"

    def __str__(self):
        return f"{self.titulo} ({self.get_tipo_display()})"

    def clean(self):
        # Validação para garantir que apenas um dos campos (arquivo ou url) seja preenchido
        if self.tipo == self.TipoRecurso.DOWNLOAD and not self.arquivo:
            from django.core.exceptions import ValidationError
            raise ValidationError({'arquivo': _('Para um recurso de Download, um arquivo é obrigatório.')})
        if self.tipo == self.TipoRecurso.LINK and not self.url:
            from django.core.exceptions import ValidationError
            raise ValidationError({'url': _('Para um recurso de Link Externo, uma URL é obrigatória.')})
        if self.tipo == self.TipoRecurso.DOWNLOAD and self.url:
            from django.core.exceptions import ValidationError
            raise ValidationError({'url': _('Um recurso de Download não pode ter uma URL. Use o campo "arquivo".')})
        if self.tipo == self.TipoRecurso.LINK and self.arquivo:
            from django.core.exceptions import ValidationError
            raise ValidationError({'arquivo': _('Um recurso de Link Externo não pode ter um arquivo. Use o campo "url".')})