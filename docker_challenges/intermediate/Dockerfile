FROM debian:bullseye

LABEL maintainer="admin@ctf-platform.local"

# Installation de VSFTPD (serveur FTP) et d'autres outils
RUN apt-get update && apt-get install -y \
    vsftpd \
    && rm -rf /var/lib/apt/lists/*

# Copier les fichiers de configuration
COPY vsftpd.conf /etc/vsftpd.conf
RUN echo "ctfuser:FLAG{intermediate_level_ctf}" | chpasswd

# Création d'un utilisateur fictif pour les défis
RUN useradd -m ctfuser

# Exposer le port pour FTP
EXPOSE 21

# Commande pour démarrer le service
CMD ["vsftpd", "/etc/vsftpd.conf"]
