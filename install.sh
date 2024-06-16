#!/bin/bash

# Paso 1: Actualización del gestor de paquetes e instalación de dependencias
echo "Actualizando el gestor de paquetes e instalando dependencias..."
sudo apt update
sudo apt install -y git python3 python3-pip uwsgi uwsgi-plugin-python3 nginx postgresql postgresql-contrib libpq-dev unzip

# Verifica si pip3 se instaló correctamente
if ! command -v pip3 &> /dev/null; then
    echo "pip3 no se instaló correctamente. Intenta instalarlo manualmente con 'sudo apt install python3-pip'."
    exit 1
fi

# Paso 2: Descargar el repositorio y moverlo a la ruta específica
echo "Clonando el repositorio y moviéndolo a la ruta específica..."
REPO_DIR="/var/www/html/PDjango/Django_PDF_Signature"
if [ -d "$REPO_DIR" ]; then
    echo "El directorio $REPO_DIR ya existe. Borrando el contenido existente..."
    sudo rm -rf "$REPO_DIR"
fi
git clone https://github.com/EnriqueSLsys/Django_PDF_Signature.git /var/www/html/PDjango/Django_PDF_Signature

# Paso 3: Instalación de requisitos de la aplicación Django
echo "Instalando requisitos de la aplicación Django..."
cd /var/www/html/PDjango/Django_PDF_Signature
if [ -f "requirements.txt" ]; then
    sudo pip3 install -r requirements.txt
else
    echo "Error: No se encontró el archivo requirements.txt."
    exit 1
fi

# Paso 4: Configuración de PostgreSQL
echo "Configurando PostgreSQL..."
sudo -i -u postgres bash << EOF
psql -c "ALTER USER postgres PASSWORD 'usuario';"
psql -c "CREATE DATABASE forms_medinaazahara;"
psql -c "GRANT ALL PRIVILEGES ON DATABASE forms_medinaazahara TO postgres;"
EOF

# Obtener la IP del equipo
IP=$(hostname -I | awk '{print $1}')

# Modificación del archivo postgresql.conf
echo "Modificando postgresql.conf..."
sudo sed -i "/^#listen_addresses =/c\listen_addresses = '$IP'" /etc/postgresql/14/main/postgresql.conf

# Modificación del archivo pg_hba.conf
echo "Modificando pg_hba.conf..."
echo "host all all $IP/24 md5" | sudo tee -a /etc/postgresql/14/main/pg_hba.conf

# Reiniciar PostgreSQL
echo "Reiniciando PostgreSQL..."
sudo systemctl restart postgresql

# Paso 5: Configuración de Nginx
echo "Configurando Nginx..."
sudo openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /etc/ssl/private/ssl-cert-snakeoil.key -out /etc/ssl/certs/ssl-cert-snakeoil.pem -subj "/CN=$IP"

NGINX_CONF="/etc/nginx/sites-available/forms_medinaazahara.conf"
sudo tee $NGINX_CONF <<EOF
server {
    listen 80;
    server_name $IP;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name $IP;

    ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
    ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

    location / {
        include uwsgi_params;
        uwsgi_pass unix:/var/www/html/PDjango/Django_PDF_Signature/formproject.sock;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
        proxy_set_header Referer \$http_referer;
    }

    location /static/ {
        alias /var/www/html/PDjango/Django_PDF_Signature/f_solicitudes/static/;
    }
}
EOF

# Activar el sitio en Nginx y reiniciar Nginx
echo "Activando el sitio en Nginx y reiniciando..."
sudo ln -s $NGINX_CONF /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Paso 6: Modificación de configuraciones en settings.py
echo "Modificando configuraciones en settings.py..."
SETTINGS_PY="/var/www/html/PDjango/Django_PDF_Signature/Django_PDF_Signature/settings.py"
if [ -f "$SETTINGS_PY" ]; then
    sudo sed -i "s/ALLOWED_HOSTS = .*/ALLOWED_HOSTS = ['localhost', '127.0.0.1', '$IP']/g" $SETTINGS_PY
    sudo sed -i "s/CSRF_TRUSTED_ORIGINS = .*/CSRF_TRUSTED_ORIGINS = ['https:\/\/$IP']/g" $SETTINGS_PY
    sudo sed -i "s/'HOST': .*/'HOST': '$IP',/g" $SETTINGS_PY
    sudo sed -i "s/'PASSWORD': .*/'PASSWORD': 'usuario',/g" $SETTINGS_PY
else
    echo "Error: No se encontró el archivo settings.py."
    exit 1
fi

# Paso 7: Migraciones de la BD del proyecto
echo "Realizando migraciones de la base de datos..."
if [ -f "manage.py" ]; then
    python3 manage.py makemigrations
    python3 manage.py migrate
else
    echo "Error: No se encontró el archivo manage.py."
    exit 1
fi

# Paso 8: Iniciar uWSGI
echo "Iniciando uWSGI..."
if [ -f "uwsgi.ini" ]; then
    sudo uwsgi --ini uwsgi.ini --plugin python3
else
    echo "Error: No se encontró el archivo uwsgi.ini."
    exit 1
fi

echo "El script ha finalizado. Accede a https://$IP para comprobar el funcionamiento."
