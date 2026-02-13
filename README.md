# 📦 Application de gestion de stock (Python + MySQL)

Cette application permet de gérer un stock de produits avec catégories et mouvements.  
Elle est conçue pour une **structure solidaire ou petite entreprise** et fonctionne en **ligne de commande**.

Avec ce programme, vous pouvez :

- Ajouter, modifier et supprimer des catégories
- Ajouter, modifier et supprimer des produits
- Gérer les mouvements de stock (ajout/retrait)
- Suivre l’historique des mouvements
- Identifier par des alertes les produits en rupture ou faible stock

---

## 🗄️ Base de données MySQL

Le projet utilise MySQL pour stocker toutes les données dans trois tables principales :  

### Tables

#### 1. `Categories`
- `id_categorie` : identifiant unique (auto-increment)
- `nom_categorie` : nom de la catégorie
- `description_categorie` : description de la catégorie

#### 2. `Produits`
- `id_produit` : identifiant unique (auto-increment)
- `designation` : nom du produit
- `prix` : prix du produit
- `id_categorie` : référence à la catégorie
- `statut` : disponible / en rupture

#### 3. `Mouvements`
- `id_mouvement` : identifiant unique (auto-increment)
- `quantite` : nombre d’unités ajoutées ou retirées
- `action` : type d’opération (`ajout` ou `retrait`)
- `id_produit` : référence au produit
- `dateheure` : date et heure du mouvement

### Exemple de création de la base

```sql
CREATE DATABASE IF NOT EXISTS stock_db;
USE stock_db;

CREATE TABLE Categories(
    id_categorie INT AUTO_INCREMENT PRIMARY KEY,
    nom_categorie VARCHAR(100) NOT NULL,
    description_categorie TEXT
);

CREATE TABLE Produits(
    id_produit INT AUTO_INCREMENT PRIMARY KEY,
    designation VARCHAR(100) NOT NULL,
    prix DECIMAL(10,2),
    id_categorie INT,
    statut ENUM('disponible','en rupture') DEFAULT 'disponible',
    FOREIGN KEY (id_categorie) REFERENCES Categories(id_categorie)
);

CREATE TABLE Mouvements(
    id_mouvement INT AUTO_INCREMENT PRIMARY KEY,
    quantite INT NOT NULL,
    action ENUM('ajout','retrait'),
    id_produit INT,
    dateheure DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_produit) REFERENCES Produits(id_produit)
);
