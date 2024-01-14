FROM python:3.9-slim

# Installer les dépendances nécessaires pour Flask
RUN apt-get update && \
    apt-get install -y curl && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de dépendances et installer les dépendances Python
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copier le reste des fichiers de l'application
COPY . .

# Exposer le port sur lequel Flask s'exécute
EXPOSE 5000

# Commande pour lancer l'application Flask
CMD ["python", "app.py"]
