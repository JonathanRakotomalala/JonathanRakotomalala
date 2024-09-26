-- Insertion de données dans la table Donateurs
INSERT INTO Donateurs (nom_donateur, adresse_donateur, date_insc_donateur) VALUES
    ('John Doe', '123 Rue des Fleurs', '2023-01-15'),
    ('Alice Smith', '456 Avenue des Etoiles', '2023-02-20'),
    ('Bob Johnson', '789 Boulevard du Soleil', '2023-03-25');

-- Insertion de données dans la table Produits
INSERT INTO Produits (code_produit, designation, type) VALUES
    ('P001', 'Pommes', 'Frais'),
    ('P002', 'Riz', 'Conserve'),
    ('P003', 'Poisson', 'Surgele'),
    ('P004', 'Lait','Frais');

-- Insertion de données dans la table Beneficiaires
INSERT INTO Beneficiaires (nom_beneficiaire, adresse_beneficiaire, date_insc_beneficiaire) VALUES
    ('Marie Dupont', '321 Rue des Arbres', '2023-01-20'),
    ('Paul Martin', '654 Avenue des Nuages', '2023-02-25'),
    ('Sophie Dubois', '987 Boulevard de la Lune', '2023-03-30');

-- Insertion de données dans la table Dons
INSERT INTO Dons (description, date_don, id_donateur) VALUES
    ('Don de pommes', '2023-02-10', 1),
    ('Don de riz', '2023-03-15', 2),
    ('Don de poisson', '2023-04-20', 3);

-- Insertion de données dans la table ProduitsDons
INSERT INTO ProduitsDons (code_produit, quantite_produit, date_peremption)
VALUES
    ('P001', 20, '2023-02-28'),
    ('P002', 30, '2023-03-31'),
    ('P003', 25, '2023-04-30');

-- Insertion de données dans la table Transactions
INSERT INTO Transactions (date_transaction, quantite_produit, code_produit, id_beneficiaire) VALUES
    ('2023-01-25', 10, 'P001', 1),
    ('2023-02-28', 20, 'P002', 2),
    ('2023-03-30', 15, 'P003', 3);
