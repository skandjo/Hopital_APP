-- Supprimer les tables existantes si elles existent déjà
DROP TABLE IF EXISTS hospitalisation CASCADE;
DROP TABLE IF EXISTS consultations CASCADE;
DROP TABLE IF EXISTS chambres CASCADE;
DROP TABLE IF EXISTS departements CASCADE;
DROP TABLE IF EXISTS medecins CASCADE;
DROP TABLE IF EXISTS patients CASCADE;


-- Création de la table des patients --
CREATE TABLE patients (
  id SERIAL PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  prenom VARCHAR(50) NOT NULL,
  date_naissance DATE NOT NULL,
  sexe CHAR(1),  -- 'M' pour masculin, 'F' pour féminin, etc.
  adresse VARCHAR(255),
  telephone VARCHAR(15),
  email VARCHAR(50),
  num_securite_social VARCHAR(50),
  contact_urgence_nom VARCHAR(50),
  contact_urgence_telephone VARCHAR(15)
);

-- Création de la table des médecins --
CREATE TABLE medecins (
  id SERIAL PRIMARY KEY,
  nom VARCHAR(50) NOT NULL,
  prenom VARCHAR(50) NOT NULL,
  date_naissance DATE NOT NULL,
  sexe CHAR(1),  -- 'M' pour masculin, 'F' pour féminin
  adresse VARCHAR(255),
  telephone VARCHAR(15),
  email VARCHAR(50),
  specialite VARCHAR(100),
  salaire DECIMAL(10, 2),
  date_embauche DATE NOT NULL,
  etat VARCHAR(10) CHECK (etat IN ('congés', 'actif')) -- 'congés' ou 'actif'
);

-- Création de la table des départements --
CREATE TABLE departements (
  id SERIAL PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  description TEXT,
  telephone VARCHAR(15),
  chef_id INTEGER REFERENCES medecins(id) ON DELETE SET NULL  -- Chef du département
);

-- Création de la table des chambres --
CREATE TABLE chambres (
  id SERIAL PRIMARY KEY,
  num_chambre VARCHAR(5) NOT NULL,
  departement_id INTEGER REFERENCES departements(id) ON DELETE SET NULL,
  patient_id INTEGER REFERENCES patients(id) ON DELETE SET NULL,  -- Le patient occupant la chambre
  disponibilite BOOLEAN NOT NULL DEFAULT TRUE  -- Indique si la chambre est disponible
);

-- Création de la table des consultations --
CREATE TABLE consultations (
  id SERIAL PRIMARY KEY,
  patient_id INTEGER NOT NULL,
  medecin_id INTEGER NOT NULL,
  date_consultation DATE NOT NULL,
  diagnostic TEXT,
  traitement_prescrit TEXT,
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
  FOREIGN KEY (medecin_id) REFERENCES medecins(id) ON DELETE CASCADE
);

-- Création de la table des hospitalisations --
CREATE TABLE hospitalisation (
  id SERIAL PRIMARY KEY,
  patient_id INTEGER NOT NULL,
  chambre_id INTEGER NOT NULL,
  date_hospitalisation DATE NOT NULL,
  diagnostic TEXT,
  traitement_prescrit TEXT,
  FOREIGN KEY (patient_id) REFERENCES patients(id) ON DELETE CASCADE,
  FOREIGN KEY (chambre_id) REFERENCES chambres(id) ON DELETE CASCADE
);

-- Insertion de données fictives --

-- Patients
INSERT INTO patients (nom, prenom, date_naissance, sexe, adresse, telephone, email, num_securite_social, contact_urgence_nom, contact_urgence_telephone)
VALUES ('Dupont', 'Jean', '1985-04-23', 'M', '10 rue de Paris, Paris', '0123456789', 'jean.dupont@email.com', '123456789012345', 'Pierre Dupont', '0601020304');

-- Médecins
INSERT INTO medecins (nom, prenom, date_naissance, sexe, adresse, telephone, email, specialite, salaire, date_embauche, etat)
VALUES ('Leclerc', 'Pierre', '1975-05-12', 'M', '15 rue des Lilas, Paris', '0147852369', 'pierre.leclerc@hopital.com', 'Cardiologue', 5000.00, '2010-06-01', 'actif'),
       ('Martin', 'Sophie', '1980-02-22', 'F', '30 rue de la République, Lyon', '0134567890', 'sophie.martin@hopital.com', 'Pédiatre', 4500.00, '2012-03-15', 'congés');

-- Départements
INSERT INTO departements (nom, description, telephone, chef_id)
VALUES ('Cardiologie', 'Spécialité des maladies cardiaques', '0147852369', 1),  -- Le chef du département est le médecin avec id 1
       ('Pédiatrie', 'Soins aux enfants', '0156789234', 2);

-- Chambres
INSERT INTO chambres (num_chambre, departement_id, disponibilite)
VALUES ('101', 1, TRUE),
       ('102', 2, FALSE);  -- Indique que la chambre 102 est occupée

-- Consultations
INSERT INTO consultations (patient_id, medecin_id, date_consultation, diagnostic, traitement_prescrit)
VALUES (1, 1, '2024-12-10', 'Hypertension', 'Médicaments anti-hypertenseurs');

-- Hospitalisations
INSERT INTO hospitalisation (patient_id, chambre_id, date_hospitalisation, diagnostic, traitement_prescrit)
VALUES (1, 1, '2024-12-10', 'Chirurgie cardiaque', 'Antibiotiques et soins post-opératoires');
