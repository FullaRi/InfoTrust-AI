# Mise en place de N8N

## Description
**N8N** est une plateforme d’automatisation de workflows. Dans le cadre de la solution InfoTrust AI, elle est utilisée pour la mise en place et l’orchestration de nos différents systèmes d’IA agentique.

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
cd infrotrustai/n8n
```

Le dépôt contient tous les fichiers nécessaires au déploiement, incluant le `docker-compose.yml`.

### Étape 2 : Configuration des variables d'environnement

#### Configuration de l'application (.env)

Copiez le fichier de configuration distribué et éditez-le selon vos besoins :

```bash
cp .env.dist .env
nano .env  # ou utilisez votre éditeur préféré
```

**Variables principales à configurer :**

Les variables les plus importantes à paramétrer sont les suivantes :

| Variable                    | Description                                           | Exemple                          |
|-----------------------------|-------------------------------------------------------|----------------------------------|
| `N8N_HOST`                  | Adresse ou domaine du service n8n                     | `192.168.192.192`                |
| `N8N_PORT`                  | Port d’exposition du service web                      | `5678`                          |
| `WEBHOOK_URL`               | URL publique utilisée (ou adresse ) pour les webhooks n8n           | `http://192.168.192.192/`    |



### Étape 3 : Lancement du conteneur

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
http://<adresse_ip_du_serveur>:5678
```



