FROM ubuntu:20.04

LABEL maintainer="admin@ctf-platform.local"

# Installer Apache, PHP, et MySQL
RUN apt-get update && apt-get install -y \
    apache2 \
    php \
    mysql-server \
    libapache2-mod-php \
    && rm -rf /var/lib/apt/lists/*

# Activer le module Apache pour PHP
RUN a2enmod php7.4

# Copier les fichiers vulnérables de l'application
COPY advanced_app/ /var/www/html/

# Exposer le port pour HTTP
EXPOSE 80

# Commande pour démarrer Apache en arrière-plan
CMD ["apachectl", "-D", "FOREGROUND"]
