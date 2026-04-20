# Mise en place de N8N

## Description
**N8N** est une plateforme d’automatisation de workflows. Dans le cadre de la solution InfoTrust AI, elle est utilisée pour la mise en place et l’orchestration de nos différents systèmes d’IA agentique.

### Étape 1 : Configuration des variables d'environnement

#### Configuration de l'application (.env)

Copiez le fichier de configuration distribué et éditez-le selon vos besoins :

```bash
cp .env.dist .env
nano .env  # ou utilisez votre éditeur préféré
```

**Variables principales à configurer :**

Les variables les plus importantes à paramétrer sont les suivantes :

| Variable                    | Description                                               | Exemple             |
|-----------------------------|-----------------------------------------------------------|---------------------|
| `N8N_HOST`                  | Adresse ip ou domaine du service n8n                      | `127.0.0.1`         |
| `N8N_PORT`                  | Port d’exposition du service web                          | `5678 par default`  |
| `WEBHOOK_URL`               | URL publique utilisée (ou adresse ) pour les webhooks n8n | `http://127.0.0.1/` |


### Étape 2 : Lancement du conteneur

Démarrez l'application et ses services en arrière-plan :

```bash
docker compose up -d
```

### Étape 3 : Vérification du déploiement

Vérifiez que les conteneurs sont actifs :

```bash
docker compose ps
```

Tous les services doivent apparaître comme "running".

Accédez à l'interface web via votre navigateur :

```
http://<adresse_ip_du_serveur>:5678
```
### Étape 5 : Création du compte administrateur n8n

Lors de la première connexion à la plateforme, vous serez invité à créer un compte administrateur.

### Étape 6 : Importation du workflow InfoTrust AI

Procédez au chargement du workflow InfoTrust AI. Celui-ci est disponible dans le fichier suivant :

`modules/web_investigation/web_investigation_n8n_ai_workflow.json`

Suivez les étapes ci-dessous pour importer le workflow `web_investigation_n8n_ai_workflow.json` dans n8n :

1. Connectez-vous à votre interface n8n (généralement accessible via `http://localhost:5678` ou le port configuré).

2. Dans le menu latéral gauche, cliquez sur **"Workflows"**.

3. Cliquez sur le bouton **"Import from File"** (Importer depuis un fichier) ou sur l'icône **"..."** (Plus d'options) puis sélectionnez **"Import"**.

4. Sélectionnez le fichier `web_investigation_n8n_ai_workflow.json` situé dans le dossier `modules/web_investigation/`.

5. Une fois le fichier chargé, le workflow apparaîtra dans la liste. Cliquez dessus pour l'ouvrir dans l'éditeur visuel.

### Étape 7 : Importation base de données media_bias
Pour que le workflow InfoTrust AI puisse fonctionner correctement, vous devez importer la base de données `media_bias` contenant les informations sur les médias (biais, fiabilité, fact-checking, etc.).

#### Fichier source

Le fichier CSV contenant les données est disponible à l'emplacement suivant :

`data/media_bias_data.csv`

#### Procédure d'importation

1. **Créez une nouvelle table de données** :

   - Dans l'interface, cliquez sur **"Create new data table"**

2. **Remplissez le formulaire** :

   | Champ | Valeur / Action                                                        |
   |-------|------------------------------------------------------------------------|
   | **Data table name** | `media_bias` (c'est le nom attendu par le workflow)                    |
   | **Option** | Cochez **"Import CSV"**                                                |
   | **Fichier** | Glissez-déposez `media_bias_data.csv` ou cliquez sur "click to upload" |
   | **Header row** | ✅ Cochez **"My CSV file contains a header row"**                       |

3. **Vérification post-import** :

Depuis le nœud **Check MediaBias DB**, vérifiez les points suivants :
   - La base de données `media_bias` est bien sélectionnée dans le paramètre **"Data table"**
   - Les colonnes utilisées dans les conditions (ex. : `url`, `credibility`) correspondent exactement aux noms des champs présents dans la base de données

### Étape 8 : Configuration des credentials des cles API

Avant d'exécuter le workflow, vous devez configurer les identifiants (credentials) des différentes API utilisées. Procédez comme suit :

1. Dans n8n, accédez à **"Credentials"** dans le menu latéral gauche.

2. Pour chaque service requis par le workflow (ex. : Google Gemini, Serper Auth account), modifiez le credential existant associé au nœud concerné.

3. Renseignez les informations suivantes selon l'API :

   | Service             | Champs requis                                      |
   |---------------------|----------------------------------------------------|
   | Google Gemini(PaLM) Api account         | `API Key` : (clé d'API Gemini)                     |
   | Serper Auth account | `Name` : X-API-KEY et `Value` : (clé d'API Serper) |

4. **Testez la connexion** si l'option est disponible pour valider que les clés sont actives et correctes.

5. Cliquez sur **"Save"** pour enregistrer chaque credential.

6. Retournez dans le workflow et vérifiez que chaque nœud critique (en rouge ou signalé) est bien associé au bon credential.

### Étape 9 : Publication du workflow et récupération de l'URL du webhook

Une fois le workflow configuré et testé, vous devez le publier pour le rendre accessible via un webhook.

#### Procédure

1. **Activez le workflow** :
   - Dans l'éditeur n8n, cliquez sur le bouton **"Active"** (ou le curseur d'activation) en haut à droite
   - Le workflow passe alors en mode **"Active"** (vert)

2. **Localisez le nœud Webhook** :
   - Repérez le nœud de type **"Webhook"** dans votre workflow
   - Cliquez dessus pour ouvrir ses paramètres

3. **Récupérez l'URL du webhook** :
   - Dans les paramètres du nœud Webhook, vous trouverez l'**URL d'appel** (Production URL)
   - Elle se présente généralement sous la forme :
   - `http://ip_serveur:5678/webhook/id_webhook`

4. **Notez l'URL** :
    - Conservez cette URL pour l'intégration avec les autres services InfoTrust AI
    - Elle servira de point d'entrée pour déclencher le workflow

### Étape 10 : Vérification du webhook

Vous pouvez tester le bon fonctionnement du Webhook en envoyant une requête de prédiction.

```bash
curl -X POST "http://ip_serveur:5678/webhook/id_webhook" -H "Content-Type: application/json" -d "{\"user_input\": \"NASA recently admitted in a leaked internal memo that the 1969 moon landing was filmed in a high-security studio in Nevada because the radiation belts were too deadly for astronauts to survive the journey through deep space.\"}"
```

### ⏱️ Temps d'analyse

> 💡 **Note** L'analyse prend du temps **(~7 minutes)** en fonction de la complexité du contenu à analyser.
