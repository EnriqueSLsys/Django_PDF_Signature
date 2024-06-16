# Django PDF Signature

Este proyecto es una aplicación Django para la firma de PDFs. A continuación, encontrarás las instrucciones para la instalación manual y automatizada.

## Requisitos Previos

- Ubuntu 22.04
- Python 3
- PostgreSQL
- Nginx
- uWSGI
- Git

## Instalación Manual

### Paso 1: Instalación de Dependencias

Actualiza el gestor de paquetes e instala las dependencias necesarias:

```sh
sudo apt update
sudo apt install -y git python3 python3-pip uwsgi uwsgi-plugin-python3 nginx postgresql postgresql-contrib libpq-dev unzip
```

### Paso 2: Clonar el Repositorio

Clona el repositorio desde GitHub:

```sh
git clone https://github.com/EnriqueSLsys/Django_PDF_Signature.git
```

Crea el directorio y mueve el contenido del repositorio:

```sh
sudo mkdir -p /var/www/html/PDjango
sudo mv Django_PDF_Signature /var/www/html/PDjango/
```

### Paso 3: Instalación de Requisitos de la Aplicación Django

Asegúrate de estar dentro del directorio de la aplicación Django:

```sh
cd /var/www/html/PDjango/Django_PDF_Signature
```

Instala los requisitos de la aplicación:

```sh
sudo pip3 install -r requirements.txt
```

### Paso 4: Configuración de PostgreSQL

Cambia a la cuenta de usuario postgres y configura la base de datos:

```sh
sudo -i -u postgres
psql -c "ALTER USER postgres PASSWORD 'usuario';"
psql -c "CREATE DATABASE forms_medinaazahara;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE forms_medinaazahara TO postgres;"
exit
```

Modifica el archivo `postgresql.conf`:

```sh
sudo nano /etc/postgresql/14/main/postgresql.conf
```

Añade la siguiente línea (reemplaza `TU_IP` con la IP de tu servidor):

```plaintext
listen_addresses = 'TU_IP'
```

Modifica el archivo `pg_hba.conf`:

```sh
sudo nano /etc/postgresql/14/main/pg_hba.conf
```

Añade la siguiente línea al final del archivo:

```plaintext
host all all TU_IP/24 md5
```

Reinicia PostgreSQL:

```sh
sudo systemctl restart postgresql
```

### Paso 5: Configuración de Nginx

Genera un certificado SSL autofirmado:

```sh
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/certs/ssl-cert-snakeoil.pem
```

Crea un archivo de configuración para tu sitio web en Nginx:

```sh
sudo nano /etc/nginx/sites-available/forms_medinaazahara.conf
```

Añade el siguiente contenido (reemplaza `TU_IP` con la IP de tu servidor):

```plaintext
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
        uwsgi_pass unix:/var/www/html/PDjango/Django_PDF_Signature/formproject.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $

remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Referer $http_referer;
    }

    location /static/ {
        alias /var/www/html/PDjango/Django_PDF_Signature/f_solicitudes/static/;
    }
}
```

Activa el sitio en Nginx y reinicia:

```sh
sudo ln -s /etc/nginx/sites-available/forms_medinaazahara.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

### Paso 6: Modificación de Configuraciones en settings.py

Modifica el archivo `settings.py` para adaptarlo a tu IP/Dominio:

```sh
sudo nano /var/www/html/PDjango/Django_PDF_Signature/Django_PDF_Signature/settings.py
```

Cambia las siguientes líneas:

```python
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'TU_IP']
CSRF_TRUSTED_ORIGINS = ['https://TU_IP']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'forms_medinaazahara',
        'USER': 'postgres',
        'PASSWORD': 'tu_nueva_contraseña',
        'HOST': 'TU_IP',
        'PORT': '5432',
    }
}
```

### Paso 7: Migraciones de la BD del Proyecto

Realiza las migraciones de la base de datos:

```sh
python3 /var/www/html/PDjango/Django_PDF_Signature/manage.py makemigrations
python3 /var/www/html/PDjango/Django_PDF_Signature/manage.py migrate
```

### Paso 8: Iniciar uWSGI

Inicia uWSGI:

```sh
sudo uwsgi --ini /var/www/html/PDjango/Django_PDF_Signature/uwsgi.ini --plugin python3
```

## Instalación Automatizada

Para una instalación automática, sigue estos pasos:

1. Clona el repositorio desde GitHub:

```sh
git clone https://github.com/EnriqueSLsys/Django_PDF_Signature.git
```

2. Cambia al directorio del repositorio:

```sh
cd Django_PDF_Signature
```

3. Da permisos de ejecución al script de instalación:

```sh
chmod +x install.sh
```

4. Ejecuta el script de instalación:

```sh
sudo ./install.sh
```
