// conteudos_tcc/static/conteudos_tcc/js/recurso_admin.js

(function($) {
    $(document).ready(function() {
        function toggleResourceFields() {
            var tipo = $('#id_tipo').val();
            var $arquivoField = $('.field-arquivo');
            var $urlField = $('.field-url');

            if (tipo === 'DOWNLOAD') {
                $arquivoField.show();
                $urlField.hide();
            } else if (tipo === 'LINK') {
                $arquivoField.hide();
                $urlField.show();
            } else {
                $arquivoField.hide();
                $urlField.hide();
            }
        }

        // Executa na carga da página
        toggleResourceFields();

        // Executa quando o tipo muda
        $('#id_tipo').change(function() {
            toggleResourceFields();
        });
    });
})(django.jQuery);