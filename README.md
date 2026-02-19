<p align="center">
  <img src="./docs/images/logo.png" alt="Logo InfoTrust AI" width="180"/>
</p>

<h1 align="center">InfoTrust AI</h1>
<p align="center"><strong>Système de détection de désinformation par intelligence artificielle</strong></p>

## Description
**InfoTrust AI** est une solution avancée de détection automatique de la désinformation (fake news).  
Développé dans le cadre du cours Atelier pratique II en cybersécurité à l’UQAC, le système repose sur une architecture hybride combinant :

- Une classification par Deep Learning pour l’analyse sémantique initiale
- Un moteur de raisonnement agentique pour la vérification factuelle en temps réel

Cette approche permet de produire un verdict de crédibilité fondé à la fois sur des probabilités statistiques et sur des preuves factuelles issues de sources fiables.

## 📌 Architecture

![Architecture du projet](./docs/images/global_arch.png)

## 📂 Modules

InfoTrust AI est segmenté en unités.

- [Module Core](./modules/core/README.md)
- [Module Frontend](./modules/frontend/README.md)
- [Module Investigation Web](./modules/web_investigation/README.md)
- [Module Deep Learning](./modules/deep_learning/README.md)

---
## 🔄 n8n
Certains modules d’InfoTrust AI utilisent **n8n** pour orchestrer les agents d’IA et automatiser les flux de traitement.

- [Mise en place de n8n](./n8n/README.md)
