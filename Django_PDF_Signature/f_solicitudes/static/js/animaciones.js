$(document).ready(function() {
    // Función para animar el texto del navbar-brand
    var brandText = $('#brandText');
    var text = brandText.text();
    brandText.empty();
    var i = 0;
    function typeWriter() {
        if (i < text.length) {
            brandText.append(text.charAt(i));
            i++;
            setTimeout(typeWriter, 100);
        }
    }
    typeWriter();

    // Con esta función ajuisto dinámicamente la altura del textarea usando jQuery
    $('#texto').on('input', function() {
        this.style.height = 'auto';
        // Establezco la altura máxima del textarea
        if (this.scrollHeight <= parseInt($(this).css('max-height'))) {
            this.style.height = (this.scrollHeight) + 'px';
        } else {
            this.style.overflowY = 'auto';
        }
    });
});
