# Django_PDF_Signature

## Descripción

**Django_PDF_Signature** es una plataforma web desarrollada con Django que permite la generación y firma digital de documentos PDF utilizando la herramienta Autofirma. Este proyecto está diseñado para proporcionar una solución eficiente y segura para individuos y empresas que necesitan gestionar documentos de manera digital, asegurando la autenticidad y confidencialidad de la información.

## Características

- **Generación de Documentos PDF**: Crea documentos PDF a partir de formularios web personalizados.
- **Firma Digital**: Firma documentos PDF de manera segura utilizando Autofirma.
- **Seguridad y Confidencialidad**: Incorpora medidas de seguridad robustas, incluyendo cifrado de datos, autenticación de usuarios y controles de acceso.
- **Colaboración**: Facilita la revisión y firma de documentos por múltiples usuarios con funciones de seguimiento de cambios y comentarios.

## Instalación

### Requisitos Previos

- Python 3
- PostgreSQL
- Nginx
- uWSGI
- Autofirma 1.8 o superior

### Pasos de Instalación

1. **Clonar el Repositorio desde GitHub**:

   ```bash
   git clone https://github.com/EnriqueSLsys/Django_PDF_Signature.git
   ```

2. **Crear el Directorio del Proyecto**:

   ```bash
   sudo mkdir -p /var/www/html/PDjango
   ```

3. **Mover el Repositorio Clonado**:

   ```bash
   sudo mv Django_PDF_Signature/* /var/www/html/PDjango/
   ```

4. **Instalar Dependencias**:

   ```bash
   sudo apt update
   sudo apt install python3 python3-pip uwsgi uwsgi-plugin-python3 nginx postgresql postgresql-contrib libpq-dev unzip
   sudo pip3 install -r /var/www/html/PDjango/requirements.txt
   ```

5. **Configurar PostgreSQL**:

   ```bash
   sudo -i -u postgres
   psql
   ALTER USER postgres PASSWORD 'usuario';
   CREATE DATABASE forms_tangrambpm;
   GRANT ALL PRIVILEGES ON DATABASE forms_tangrambpm TO postgres;
   \q
   exit

   sudo nano /etc/postgresql/14/main/postgresql.conf
   # Añadir:
   listen_addresses = 'TU_IP'

   sudo nano /etc/postgresql/14/main/pg_hba.conf
   # Añadir al final:
   host all all TU_IP/24 md5

   sudo systemctl restart postgresql
   ```

6. **Configurar Nginx**:
   Asegúrate de cambiar TU_IP por la IP de tu host.

   ```bash
   sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/certs/ssl-cert-snakeoil.pem

   sudo nano /etc/nginx/sites-available/formularios_tangram.conf
   # Añadir:
   server {
       listen 80;
       server_name TU_IP;
       return 301 https://$host$request_uri;
   }
   server {
       listen 443 ssl;
       server_name TU_IP;
       ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
       ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;
       location / {
           include uwsgi_params;
           uwsgi_pass unix:/var/www/html/PDjango/formularios_tangram/formproject.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
           proxy_set_header Referer $http_referer;
       }
       location /static/ {
           alias /var/www/html/PDjango/formularios_tangram/f_solicitudes/static/;
       }
   }

   sudo ln -s /etc/nginx/sites-available/formularios_tangram.conf /etc/nginx/sites-enabled/
   sudo systemctl restart nginx
   ```

7. **Modificar Configuraciones en settings.py**:

   ```bash
   sudo nano /var/www/html/PDjango/formularios_tangram/formularios_tangram/settings.py
   # Cambiar:
   ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'TU_IP']
   CSRF_TRUSTED_ORIGINS = ['https://TU_IP']
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql_psycopg2',
           'NAME': 'forms_tangrambpm',
           'USER': 'postgres',
           'PASSWORD': 'tu_nueva_contraseña',
           'HOST': 'TU_IP',
           'PORT': '5432',
       }
   }
   ```

8. **Migraciones de la Base de Datos**:

   ```bash
   python3 /var/www/html/PDjango/formularios_tangram/manage.py makemigrations
   python3 /var/www/html/PDjango/formularios_tangram/manage.py migrate
   ```

9. **Iniciar uWSGI**:

   ```bash
   uwsgi --ini /var/www/html/PDjango/formularios_tangram/uwsgi.ini --plugin python3
   ```

10. **Acceso a la Plataforma**:

    Abre un navegador web y accede a `https://TU_IP`. Deberías ver la pantalla de inicio.

## Contribución

Si deseas contribuir a este proyecto, por favor, sigue los pasos a continuación:

1. Haz un fork del repositorio.
2. Crea una nueva rama (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit (`git commit -am 'Añadir nueva funcionalidad'`).
4. Sube los cambios a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un Pull Request.

## Licencia

Este proyecto está bajo la licencia [Creative Commons BY-NC-ND 4.0 España](https://creativecommons.org/licenses/by-nc-nd/4.0/legalcode).

## Contacto

Para cualquier consulta o sugerencia, por favor contacta a Enrique Serrano Lendines en [enrique.serrano.sys@gmail.com](mailto:enrique.serrano.sys@gmail.com).
