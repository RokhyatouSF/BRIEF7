# Système de gestion de tickets – Centre de formation

## Présentation
Ce projet est une application Python connectée à MySQL permettant de gérer un système de tickets interne dans un centre de formation.  
Il simule un fonctionnement réel avec plusieurs profils d’utilisateurs et des droits d’accès précis selon le rôle.

L’objectif est de proposer un outil simple mais structuré pour :
- signaler des problèmes
- les assigner à un membre du personnel
- suivre leur traitement
- garantir la traçabilité des actions

Le système repose sur une logique professionnelle inspirée d’un environnement pédagogique réel.

---

## Rôles disponibles
Le système gère plusieurs rôles :

- apprenant  
- technicien  
- coach formateur hard skills  
- coach soft skills  
- surveillant  
- référent  
- gardien  
- admin  

Chaque rôle possède des permissions spécifiques.

---

## Fonctionnement général

### Apprenant
L’apprenant peut :
- créer un ticket
- choisir le rôle qui doit traiter sa demande
- voir la liste des utilisateurs correspondant à ce rôle
- sélectionner la personne qui prendra en charge son ticket
- suivre l’état de ses tickets

Menu apprenant :
1 Créer ticket
2 Mes tickets
0 Déconnexion


Lors de la création d’un ticket :
1. l’apprenant choisit un rôle  
2. le système affiche les utilisateurs de ce rôle  
3. il sélectionne la personne  
4. le ticket est créé avec statut **en attente**

---

### Staff (coach, technicien, référent, surveillant, gardien)
Les membres du staff peuvent :

- voir les tickets qui leur sont assignés
- consulter les informations de l’apprenant
- modifier le statut du ticket :
  - en attente
  - en cours
  - résolu
- gérer les promotions
- gérer les formations

Le niveau d’urgence d’un ticket est calculé automatiquement selon le délai maximal de traitement.

---

### Administrateur
L’administrateur possède tous les droits.

Il peut :
- voir tous les tickets
- assigner des tickets
- gérer les rôles
- gérer les promos
- gérer les formations
- consulter les logs
- voir qui a fait quoi et à quel moment

Menu admin :
1 Voir tickets assignés
3 Ajouter promo
4 Ajouter formation
5 Assigner ticket
6 Voir logs
0 Déconnexion


---

## Sécurité des données

Le système a été conçu pour garantir trois principes fondamentaux.

### Confidentialité
- mots de passe hachés avec bcrypt  
- accès contrôlé par rôle  
- authentification obligatoire  

### Intégrité
- base de données relationnelle  
- contraintes SQL  
- statuts contrôlés  
- cohérence des relations  

### Non-répudiation
Toutes les actions sont enregistrées dans une table de logs.

Chaque action conserve :
- la date
- l’utilisateur
- l’action effectuée
- le ticket concerné

Exemple d’affichage des logs pour l’administrateur :

ID Ticket : 2
Titre : Plateforme qui ne marche pas
Créé par : Rokhyatou Fall
Assigné à : Cheikh Talla
Statut : resolu
Date création : 2026-02-13 12:40:36


L’administrateur peut donc savoir précisément :
qui a créé un ticket,  
à qui il a été assigné,  
et comment il a été traité.

---

## Base de données

Tables principales :
- utilisateurs
- roles
- tickets
- demandes
- promos
- formations
- logs

Relations :
- un utilisateur possède un rôle
- un ticket est créé par un apprenant
- un ticket est assigné à un membre du staff
- chaque ticket possède un statut
- chaque action est enregistrée

---
