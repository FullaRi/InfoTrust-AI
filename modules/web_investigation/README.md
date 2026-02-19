# 📘 Module Investigation Web
Implémenté avec **n8n**, cet sous système automatise la recherche de preuves en ligne grace aux agents IA pour détecter la désinformation.

## Pré-requis
Avant de configurer ce module, assurez-vous que :  

- n8n est installé et accessible sur votre machine ou serveur.  
- Vous avez accès à l’interface Web de n8n.

## Mise en place du module

1️⃣ **Importer le workflow**

1. Ouvrez l’interface n8n dans votre navigateur.

2. Allez dans Workflows → Import.

3. Sélectionnez le fichier web_investigation_n8n_ai_workflow.json présent dans ce répertoire.

4. Cliquez sur Import pour charger le workflow.

<br>

2️⃣ **Importer les données des sources**

Le module utilise une base de données interne des médias pour vérifier la fiabilité des sources.

1. Dans n8n, creer une base de donné nommé 'media_bias'.

2. Chargez le fichier data/media_bias.csv.

💡 Le fichier contient environ 7000 sources avec leurs niveaux de biais et fiabilité.

<br>

3️⃣ **Ajouter les clés API**

Le workflow utilise des intégrations externes pour les recherches et la génération de réponses :

- Google Gemini API

&nbsp;&nbsp;&nbsp;&nbsp; 1. Dans n8n, allez dans Credentials → Create.

&nbsp;&nbsp;&nbsp;&nbsp; 2. Choisissez HTTP Request ou un nœud spécifique pour Gemini.

&nbsp;&nbsp;&nbsp;&nbsp; 3. Saisissez votre clé API Gemini.

- Serper API

Dans n8n, allez dans Credentials → Create.

Sélectionnez Header Auth ou Serper API si le nœud existe.

Entrez votre clé API Serper.

⚠️ Assurez-vous que les nœuds du workflow utilisent les bonnes credentials configurées.

<br>

4️⃣ Activer le workflow

Une fois le workflow importé et les données configurées, activez-le dans n8n.