FROM python:3.11-slim

# Installer Apache2 et mod-wsgi
RUN apt-get update && apt-get install -y \
    apache2 \
    libapache2-mod-wsgi-py3 \
    libpq-dev \
    gcc \
    && apt-get clean

# Installer les dépendances Python
COPY requirements.txt /tmp/
RUN pip3 install --upgrade pip && pip3 install -r /tmp/requirements.txt

# Créer dossier application
RUN mkdir -p /var/www/site
WORKDIR /var/www/site

# Copier le code
COPY . /var/www/site

# Collecter les fichiers statiques
RUN python3 manage.py collectstatic --noinput

# Copier config Apache
COPY apache/django.conf /etc/apache2/sites-available/000-default.conf

# Donner les bons droits
RUN chown -R www-data:www-data /var/www/site

# Activer WSGI
RUN a2enmod wsgi

EXPOSE 80

CMD ["apache2ctl", "-D", "FOREGROUND"]
