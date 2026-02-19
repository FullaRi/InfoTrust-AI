# InfoTrust AI Web

## Description
InfoTrust AI Web est l’interface web du projet InfoTrust AI, conçue pour permettre aux utilisateurs finaux 
de vérifier rapidement la fiabilité d’une information grâce à l’intelligence artificielle.

### Vérification des prérequis

Exécutez les commandes suivantes pour vérifier que Docker et Docker Compose sont correctement installés :

```bash
# Vérification de la version de Docker
docker --version

# Vérification de la version de Docker Compose
docker compose version

# Validation du statut du service Docker
sudo systemctl status docker
```

## Installation en utilisant Docker

### Étape 1 : Clonage du dépôt

Clonez le dépôt InfoTrust AI depuis GitLab :

```bash
git clone https://gitlab.com/uqac1674503/infotrustai.git
cd infrotrustai/frontend_module
```

Le dépôt contient tous les fichiers nécessaires au déploiement, incluant le `Dockerfile` et le `docker-compose.yml`.

### Étape 2 : Configuration des variables d'environnement

#### Configuration de l'application (.env)

Copiez le fichier de configuration distribué et éditez-le selon vos besoins :

```bash
cp .env.dist .env
nano .env  # ou utilisez votre éditeur préféré
```

**Variables principales à configurer :**

| Variable                    | Description                                           | Exemple                          |
|-----------------------------|-------------------------------------------------------|----------------------------------|
| `APP_PORT`                  | Port d'exposition du service web                      | `8000`                           |
| `DEBUG`                     | Mode débogage (False en production)                   | `False`                          |
| `SECRET_KEY`                | Clé cryptographique Django (unique et confidentielle) | `votre-cle-secrete-aleatoire`    |
| `API_URL`                   | URL de l'api du backend                               | `http://<adresse_ip_du_serveur>` ||
| `CONTACT_REQUEST_DST_EMAIL` | Email de destination des formulaire de contact        | `contact@example.com`            |
| `MAIL_SERVER`               | Serveur SMTP                                          | `smpt.server.com`                |
| `MAIL_PORT`                 | Port SMTP                                             | `587`                            |
| `MAIL_USE_TLS`              | Utilisation de TLS                                    | `True`                           |
| `MAIL_USERNAME`             | Compte email expéditeur                               | `noreply@example.com`            |
| `MAIL_PASSWORD`             | Mot de passe SMTP                             <br/>        | `votre-mot-de-passe`             |

**Bonnes pratiques :**
- Définissez `DEBUG=False` en production
- Utilisez une clé `SECRET_KEY` unique et complexe


### Étape 3 : Construction de l'image Docker

Construisez l'image de l'application avec Docker Compose :

```bash
docker compose build
```

Cette commande lit le `Dockerfile`, installe les dépendances Python et prépare l'environnement d'exécution.

### Étape 4 : Lancement des conteneurs

Démarrez l'application et ses services en arrière-plan :

```bash
docker compose up -d
```

### Étape 5 : Vérification du déploiement

Vérifiez que les conteneurs sont actifs :

```bash
docker compose ps
```

Tous les services doivent apparaître comme "running".

Accédez à l'interface web via votre navigateur :

```
http://<adresse_ip_du_serveur>:8000
```



