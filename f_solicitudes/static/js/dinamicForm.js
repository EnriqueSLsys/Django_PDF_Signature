$(document).ready(function() {
    // Función para mostrar mensaje de error
    function mostrarError(input, mensaje) {
        var divFeedback = input.next('.invalid-feedback');
        if (!divFeedback.length) {
            divFeedback = $('<div class="invalid-feedback"></div>');
            input.after(divFeedback);
        }
        divFeedback.text(mensaje);
        input.addClass('is-invalid');
    }

    // Función para quitar mensaje de error
    function quitarError(input) {
        var divFeedback = input.next('.invalid-feedback');
        divFeedback.text('');
        input.removeClass('is-invalid');
    }

    // Validación en tiempo real para el campo de nombre
    $('#nombre').on('input', function() {
        var nombre = $(this).val();
        if (nombre.length < 2) {
            mostrarError($(this), 'El nombre debe tener al menos 2 caracteres.');
        } else {
            quitarError($(this));
        }
    });

    // Validación en tiempo real para el campo de primer apellido
    $('#apellido1').on('input', function() {
        var apellido1 = $(this).val();
        if (apellido1.length < 2) {
            mostrarError($(this), 'El primer apellido debe tener al menos 2 caracteres.');
        } else {
            quitarError($(this));
        }
    });

    // Validación en tiempo real para el campo de DNI
    $('#dni').on('input', function() {
        var dni = $(this).val();
        if (dni.length !== 9) {
            mostrarError($(this), 'El DNI debe tener 8 números y una letra.');
        } else {
            var dniPattern = /^\d{8}[A-Za-z]$/;
            if (!dniPattern.test(dni)) {
                mostrarError($(this), 'El formato del DNI no es válido.');
            } else {
                var dniDigits = dni.slice(0, -1);
                var letrasValidas = 'TRWAGMYFPDXBNJZSQVHLCKE';
                var letraCalculada = letrasValidas[parseInt(dniDigits) % 23];
                if (dni.slice(-1).toUpperCase() !== letraCalculada) {
                    mostrarError($(this), 'La letra del DNI proporcionada no es válida.');
                } else {
                    quitarError($(this));
                }
            }
        }
    });

    // Validación en tiempo real para el campo de texto
    $('#texto').on('input', function() {
        var texto = $(this).val();
        if (texto.trim() === '') {
            mostrarError($(this), 'El texto es obligatorio y solo puede tener max (512 caracteres).');
        } else if (texto.length > 512) {
            mostrarError($(this), 'El texto no puede exceder los 512 caracteres.');
        } else {
            quitarError($(this));
        }
    });
});