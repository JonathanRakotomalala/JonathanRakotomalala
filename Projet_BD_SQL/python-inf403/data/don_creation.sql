DROP TABLE IF EXISTS Transactions;
DROP TABLE IF EXISTS ProduitsDons;
DROP TABLE IF EXISTS Beneficiaires;
DROP TABLE IF EXISTS Dons;
DROP TABLE IF EXISTS Produits;
DROP TABLE IF EXISTS Donateurs;

CREATE TABLE Donateurs (
id_donateur INTEGER PRIMARY KEY AUTOINCREMENT,
nom_donateur VARCHAR (60) NOT NULL,
adresse_donateur VARCHAR (60) NOT NULL,
date_insc_donateur DATE NOT NULL
);

CREATE TABLE Dons (
id_don INTEGER PRIMARY KEY AUTOINCREMENT,
description TEXT,
date_don DATE NOT NULL,
id_donateur INTEGER NOT NULL,
CONSTRAINT fk_dons_id_donateur FOREIGN KEY (id_donateur)
REFERENCES Donateurs (id_donateur)
);

CREATE TABLE Produits (
code_produit VARCHAR(30) NOT NULL,
designation VARCHAR(30) NOT NULL,
type TEXT CHECK(type IN ('Frais', 'Conserve', 'Surgele')),
CONSTRAINT pk_prod_code PRIMARY KEY (code_produit)
);

CREATE TABLE ProduitsDons (
id_don INTEGER PRIMARY KEY AUTOINCREMENT,
code_produit VARCHAR(30) NOT NULL,
quantite_produit INTEGER NOT NULL,
date_peremption DATE NOT NULL,
CONSTRAINT fk_pd_id_don FOREIGN KEY (id_don) REFERENCES Dons (id_don),
CONSTRAINT fk_pd_codep FOREIGN KEY (code_produit) REFERENCES Produits 
(code_produit)
);

CREATE TABLE Beneficiaires (
id_beneficiaire INTEGER PRIMARY KEY AUTOINCREMENT,
nom_beneficiaire VARCHAR(60) NOT NULL,
adresse_beneficiaire VARCHAR(60) NOT NULL,
date_insc_beneficiaire DATE NOT NULL
);

CREATE TABLE Transactions (
id_transaction INTEGER PRIMARY KEY AUTOINCREMENT,
date_transaction DATE NOT NULL,
quantite_produit INTEGER NOT NULL,
code_produit VARCHAR(30) NOT NULL,
id_beneficiaire INTEGER NOT NULL,
CONSTRAINT fk_trans_code_prod FOREIGN KEY (code_produit)
REFERENCES Produits(code_produit),
CONSTRAINT fk_trans_id_benef FOREIGN KEY (id_beneficiaire)
REFERENCES Beneficiaires(id_beneficiaire)
);
