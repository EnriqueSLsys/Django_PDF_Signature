from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.urls import reverse
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer
from reportlab.lib.units import inch
from io import BytesIO
from datetime import datetime
import os
from f_solicitudes.forms import SolicitudForm
import hashlib
from .models import Solicitud
from django.conf import settings
from django.views.generic import TemplateView
import base64
from babel.dates import format_datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

class IndexView(TemplateView):
    template_name = 't_hijas/inicio.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        solicitudes = Solicitud.objects.all()
        solicitudes_con_pdf = []
        for solicitud in solicitudes:
            if self.check_if_pdf_generated(solicitud):
                solicitud.is_signed = self.check_if_signed(solicitud)
                solicitudes_con_pdf.append(solicitud)
        context['solicitudes'] = solicitudes_con_pdf
        return context

    def check_if_pdf_generated(self, solicitud):
        unique_id = hashlib.sha256(f"{solicitud.id}".encode()).hexdigest()[:10]
        pdf_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}.pdf'
        pdf_dir = os.path.join(settings.MEDIA_ROOT, "PDFs")
        pdf_path = os.path.join(pdf_dir, pdf_filename)
        return os.path.exists(pdf_path)

    def check_if_signed(self, solicitud):
        unique_id = hashlib.sha256(f"{solicitud.id}".encode()).hexdigest()[:10]
        pdf_firmado_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}_signed.pdf'
        pdf_firmado_dir = os.path.join(settings.MEDIA_ROOT, "PDFs_signed")
        pdf_firmado_path = os.path.join(pdf_firmado_dir, pdf_firmado_filename)
        return os.path.exists(pdf_firmado_path)
    
def formulario(request):
    if request.method == 'POST':
        form = SolicitudForm(request.POST)
        if form.is_valid():
            solicitud = form.save(commit=False)
            solicitud.fecha_creacion = datetime.now()
            solicitud.save()
            return redirect('confirmacion', solicitud_id=solicitud.id)
    else:
        form = SolicitudForm()
    return render(request, 't_hijas/solicitud.html', {'form': form})

def confirmacion(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

    # Genera un identificador único basado en el ID de la solicitud
    unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]
    pdf_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}.pdf'

    # Directorio donde se guardan los PDFs generados
    pdf_dir = os.path.join(settings.MEDIA_ROOT, "PDFs")

    # Ruta completa del PDF generado
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    # Elimina el PDF si existe
    if os.path.exists(pdf_path):
        os.remove(pdf_path)

    return render(request, 't_hijas/confirmacion.html', {'solicitud': solicitud})

def descargar_pdf(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    
    # Genera un identificador único basado en el ID de la solicitud
    unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]

    # Se construye el nombre del archivo PDF
    pdf_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}.pdf'
    
    pdf_file_path = os.path.join(settings.MEDIA_ROOT, "PDFs", pdf_filename)
    
    if os.path.exists(pdf_file_path):
        with open(pdf_file_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'inline; filename="{pdf_filename}"'
            return response
    else:
        raise HttpResponse("El PDF solicitado no existe")

def guardar_pdf_firmado(request, solicitud_id):
    if request.method == 'POST':
        pdf_firmado_base64 = request.POST.get('pdf_base64', '')

        # Decodifico el PDF base64
        pdf_firmado_bytes = base64.b64decode(pdf_firmado_base64)

        # Obtengo la solicitud asociada al ID
        solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
        
        # Genero un identificador único basado en el ID de la solicitud
        unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]

        # Se construye el nombre del archivo PDF usando los datos de la solicitud
        pdf_firmado_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}_signed.pdf'
        
        # Directorio donde se guardarán los PDF firmados
        pdf_firmado_dir = os.path.join(settings.MEDIA_ROOT, "PDFs_signed")

        # Esta es la ruta completa del PDF firmado
        pdf_firmado_path = os.path.join(pdf_firmado_dir, pdf_firmado_filename)

        # Se guarda el PDF firmado en el sistema de archivos
        with open(pdf_firmado_path, 'wb') as f:
            f.write(pdf_firmado_bytes)

        return HttpResponse('PDF firmado guardado correctamente.')
    else:
        return HttpResponse('Error: Esta vista solo acepta solicitudes POST.')

def descargar_pdf_firmado(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    
    unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]

    pdf_firmado_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}_signed.pdf'
    
    pdf_firmado_dir = os.path.join(settings.MEDIA_ROOT, "PDFs_signed")

    pdf_firmado_path = os.path.join(pdf_firmado_dir, pdf_firmado_filename)

    if os.path.exists(pdf_firmado_path):
        with open(pdf_firmado_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{pdf_firmado_filename}"'
            return response
    else:
        return HttpResponse("El PDF firmado solicitado no existe.")

def mostrar_pdf_firmado(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)

    unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]

    pdf_firmado_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}_signed.pdf'

    # Directorio donde se guardan los PDF firmados
    pdf_firmado_dir = os.path.join(settings.MEDIA_ROOT, "PDFs_signed")

    # Ruta completa del PDF firmado
    pdf_firmado_path = os.path.join(pdf_firmado_dir, pdf_firmado_filename)

    if os.path.exists(pdf_firmado_path):
        # Si el PDF firmado existe, renderiza la plantilla pdf_firmado.html y pasa los datos del PDF firmado como contexto
        with open(pdf_firmado_path, 'rb') as pdf_file:
            pdf_base64 = base64.b64encode(pdf_file.read()).decode('utf-8')
            pdf_descarga = reverse('descargar_pdf', args=[solicitud_id])
            pdf_firmado_descarga = reverse('descargar_pdf_firmado', args=[solicitud_id])
            return render(request, 't_hijas/pdf_firmado.html', {'pdf_base64': pdf_base64, 'pdf_descarga': pdf_descarga, 'pdf_firmado_descarga': pdf_firmado_descarga})
    else:
        return HttpResponse("El PDF firmado solicitado no existe.")

def register_view(request):
    return render(request, 't_hijas/logIn_Register/register.html')

def login_view(request):
    return render(request, 't_hijas/logIn_Register/login.html')

def generar_pdf(request, solicitud_id):
    solicitud = get_object_or_404(Solicitud, pk=solicitud_id)
    
    # Generar un identificador único basado en el ID de la solicitud
    unique_id = hashlib.sha256(f"{solicitud_id}".encode()).hexdigest()[:10]
    pdf_filename = f'solicitud_{solicitud.nom}_{solicitud.ap1}_{solicitud.ap2}_{solicitud.dni}_{unique_id}.pdf'
    
    # Estilos para el PDF
    styles = getSampleStyleSheet()
    azul_oscuro = colors.HexColor("#000080")
    estilo_encabezado = ParagraphStyle(
        name='Encabezado',
        parent=styles['Title'],
        fontSize=16,
        textColor=azul_oscuro,
        spaceAfter=10,
    )
    estilo_bienvenida = ParagraphStyle(
        name='Bienvenida',
        parent=styles['Normal'],
        fontSize=14,
        textColor=colors.HexColor("#333333"),
        spaceAfter=10,
    )
    estilo_cuerpo = ParagraphStyle(
        name='Cuerpo',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=10,
    )
    estilo_fecha = ParagraphStyle(
        name='Fecha',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.gray,
        spaceAfter=12,
    )

    # Directorios
    pdf_Dir = "PDFs"
    img_Dir = "IMGs"
    
    # Agregar logo de Tangram
    logo_path = os.path.join(settings.MEDIA_ROOT, img_Dir, 'IESmedina_pdf.png')
    
    # Definir un tamaño fijo para la imagen
    logo_width = 1.5 * inch
    logo_height = 0.75 * inch

    buffer = BytesIO()

    # Crear una plantilla de página que incluya el encabezado y el pie de página
    def agregar_encabezado(canvas, doc):
        canvas.saveState()
        # Añadir imagen del logo en el encabezado
        canvas.drawImage(logo_path, doc.leftMargin, doc.pagesize[1] - 1 * inch, width=logo_width, height=logo_height)
        canvas.restoreState()

    def agregar_pie_de_pagina(canvas, doc):
        canvas.saveState()
        # Añadir imagen del logo en el pie de página
        canvas.drawImage(logo_path, doc.leftMargin, 0.5 * inch, width=logo_width, height=logo_height)
        canvas.restoreState()

    # Crear el documento con marcos que excluyen el área del encabezado y el pie de página
    doc = BaseDocTemplate(buffer, pagesize=letter, title=pdf_filename)
    frame = Frame(doc.leftMargin, doc.bottomMargin + inch, doc.width, doc.height - 2 * inch, id='normal')
    template = PageTemplate(id='test', frames=[frame], onPage=agregar_encabezado, onPageEnd=agregar_pie_de_pagina)
    doc.addPageTemplates([template])

    # Formatear la fecha en español
    fecha_creacion = format_datetime(solicitud.fecha_creacion, "d 'de' MMMM 'de' yyyy 'a las' H:mm:ss", locale='es_ES')

    # Añadir el contenido
    contenido = [
        Spacer(1, logo_height + 10),  # Espacio para el encabezado
        Paragraph(f'Estimado {solicitud.nom} {solicitud.ap1} {solicitud.ap2}, con DNI: {solicitud.dni}', estilo_encabezado),
        Spacer(1, 8),
        Paragraph('A continuación, recogemos el texto de su solicitud:', estilo_bienvenida),
        Spacer(1, 8),
        Paragraph(solicitud.texto, estilo_cuerpo),
        Spacer(1, 8),
        Paragraph(f'Dándole las gracias, atentamente, {fecha_creacion}', estilo_fecha),
    ]

    doc.build(contenido)

    # Convertir el PDF a Base64
    pdf_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Guardar el PDF Base64 en el contexto para pasarlo al template
    pdf_base64_context = f"{pdf_base64}"

    pdf_file_path = os.path.join(settings.MEDIA_ROOT, pdf_Dir, pdf_filename)
    with open(pdf_file_path, 'wb') as f:
        f.write(buffer.getvalue())

    pdf_url = reverse('descargar_pdf', args=[solicitud_id])
    guardar_pdf_firmado_url = reverse('guardar_pdf_firmado', args=[solicitud_id])

    return render(request, 't_hijas/generar_pdf.html', {
        'solicitud': solicitud,
        'pdf_url': pdf_url,
        'guardar_pdf_firmado_url': guardar_pdf_firmado_url,
        'pdf_base64': pdf_base64_context
    })


def register_view(request):
    return render(request, 't_hijas/logIn_Register/register.html')

def login_view(request):
    return render(request, 't_hijas/logIn_Register/login.html')

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'El nombre de usuario ya está en uso')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'El correo electrónico ya está en uso')
                return redirect('register')
            else:
                user = User.objects.create_user(username=username, email=email, password=password1)
                user.save()
                messages.success(request, 'Tu cuenta ha sido creada exitosamente')
                return redirect('login')
        else:
            messages.error(request, 'Las contraseñas no coinciden')
            return redirect('register')
    else:
        return redirect('register')

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenido {username}')
            return redirect('solicitudes')  # Redirige a la página principal después de iniciar sesión
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos')
            return redirect('login')
    else:
        return redirect('login')