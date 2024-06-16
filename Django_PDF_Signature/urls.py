from django.contrib import admin
from django.urls import path
from f_solicitudes.views import (
    IndexView, formulario, confirmacion, generar_pdf, descargar_pdf, 
    guardar_pdf_firmado, descargar_pdf_firmado, mostrar_pdf_firmado, 
    register_view, login_view, register_user, login_user
)

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('formulario/', formulario, name='solicitudes'),
    path('confirmacion/<int:solicitud_id>/', confirmacion, name='confirmacion'),
    path('generar_pdf/<int:solicitud_id>/', generar_pdf, name='generar_pdf'),
    path('descargar_pdf/<int:solicitud_id>/', descargar_pdf, name='descargar_pdf'),
    path('guardar_pdf_firmado/<int:solicitud_id>/', guardar_pdf_firmado, name='guardar_pdf_firmado'),
    path('descargar-pdf-firmado/<int:solicitud_id>/', descargar_pdf_firmado, name='descargar_pdf_firmado'),
    path('mostrar_pdf_firmado/<int:solicitud_id>/', mostrar_pdf_firmado, name='mostrar_pdf_firmado'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('register_user/', register_user, name='register_user'),
    path('login_user/', login_user, name='login_user'),
]
