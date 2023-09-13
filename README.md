# Projet7

Ce dépôt GitHub fait parti du Projet 7 de la formation Data Scientist OpenClassRooms.
Le projet est composé de plusieurs partie :
* [API](https://github.com/OPouillot/API_P7)
* Dashboard

## Description du projet

La société financière "Prêt à dépenser", propose des crédits à la consommation pour des personnes ayant peu ou pas du tout d'historique de prêt.
L’entreprise souhaite mettre en œuvre un outil de scoring crédit qui calcule la probabilité qu’un client rembourse son crédit, puis classifie la demande en crédit accordé ou refusé. Elle souhaite donc développer un algorithme de classification en s'appuyant sur des sources de données variées (données comportementales, données provenant d'autres institutions financières, etc.).

Les données originales sont téléchargeables sur Kaggle à [cette adresse](https://www.kaggle.com/competitions/home-credit-default-risk/data)

## Dashboard - Fonctionnement

Ce dépôt compose la partie Dashboard. Pour le faire fonctionner, il faut suivre les étapes dans l'ordre :
* Installer l'environnement de développement et installer les librairies via la liste __requirements.txt__
* Suite à un push GitHub sur la branch updates, les GitHub actions vont déployer le dashboard sur Streamlit à [cette adresse](https://tatave76-dashboard-p7-dashboard-bsgxhs.streamlit.app/)