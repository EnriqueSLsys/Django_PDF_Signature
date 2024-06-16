#!/bin/bash

echo "Actualizando el gestor de paquetes e instalando dependencias..."
sudo apt update --fix-missing
sudo apt install -y git python3 python3-pip uwsgi uwsgi-plugin-python3 nginx postgresql postgresql-contrib libpq-dev unzip

# Verificar la instalación de los paquetes esenciales
if ! command -v pip3 &> /dev/null
then
    echo "pip3 no se pudo instalar. Por favor, verifica los repositorios."
    exit 1
fi

if ! command -v uwsgi &> /dev/null
then
    echo "uwsgi no se pudo instalar. Por favor, verifica los repositorios."
    exit 1
fi

if ! command -v psql &> /dev/null
then
    echo "PostgreSQL no se pudo instalar. Por favor, verifica los repositorios."
    exit 1
fi

# Clonar el repositorio
REPO_DIR="/var/www/html/PDjango/Django_PDF_Signature"
if [ -d "$REPO_DIR" ]; then
    echo "El directorio $REPO_DIR ya existe. Borrando el contenido existente..."
    sudo rm -rf "$REPO_DIR"
fi

echo "Clonando el repositorio y moviéndolo a la ruta específica..."
git clone https://github.com/EnriqueSLsys/Django_PDF_Signature.git "$REPO_DIR"

# Verificar si el repositorio se clonó correctamente
if [ ! -d "$REPO_DIR" ]; then
    echo "Error: El repositorio no se pudo clonar correctamente."
    exit 1
fi

# Entrar en el directorio del repositorio
cd "$REPO_DIR"

echo "Instalando requisitos de la aplicación Django..."
if [ -f "requirements.txt" ]; then
    sudo pip3 install -r requirements.txt
else
    echo "Error: No se encontró el archivo requirements.txt."
    exit 1
fi

echo "Configurando PostgreSQL..."
sudo -i -u postgres psql -c "ALTER USER postgres PASSWORD 'usuario';"
sudo -i -u postgres psql -c "CREATE DATABASE forms_medinaazahara;"
sudo -i -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE forms_medinaazahara TO postgres;"

echo "Modificando postgresql.conf..."
sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/g" /etc/postgresql/14/main/postgresql.conf

echo "Modificando pg_hba.conf..."
echo "host all all 192.168.1.18/24 md5" | sudo tee -a /etc/postgresql/14/main/pg_hba.conf

echo "Reiniciando PostgreSQL..."
sudo systemctl restart postgresql

echo "Configurando Nginx..."
sudo bash -c 'cat > /etc/nginx/sites-available/forms_medinaazahara.conf <<EOL
server {
    listen 80;
    server_name 192.168.1.18;
    return 301 https://\$host\$request_uri;
}

server {
    listen 443 ssl;
    server_name 192.168.1.18;

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
EOL'

echo "Activando el sitio en Nginx y reiniciando..."
sudo ln -s /etc/nginx/sites-available/forms_medinaazahara.conf /etc/nginx/sites-enabled/
sudo systemctl restart nginx

echo "Modificando configuraciones en settings.py..."
SETTINGS_FILE="$REPO_DIR/Django_PDF_Signature/settings.py"
if [ -f "$SETTINGS_FILE" ]; then
    sudo sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = ['localhost', '127.0.0.1', '192.168.1.18']/g" "$SETTINGS_FILE"
    sudo sed -i "s/CSRF_TRUSTED_ORIGINS = \[\]/CSRF_TRUSTED_ORIGINS = ['https:\/\/192.168.1.18']/g" "$SETTINGS_FILE"
    sudo sed -i "s/'HOST': 'localhost'/'HOST': '192.168.1.18'/g" "$SETTINGS_FILE"
    sudo sed -i "s/'PASSWORD': ''/'PASSWORD': 'usuario'/g" "$SETTINGS_FILE"
else
    echo "Error: No se encontró el archivo settings.py."
    exit 1
fi

echo "Realizando migraciones de la base de datos..."
if [ -f "manage.py" ]; then
    python3 manage.py makemigrations
    python3 manage.py migrate
else
    echo "Error: No se encontró el archivo manage.py."
    exit 1
fi

echo "Iniciando uWSGI..."
sudo uwsgi --ini "$REPO_DIR/uwsgi.ini" --plugin python3

echo "El script ha finalizado. Accede a https://192.168.1.18 para comprobar el funcionamiento."
