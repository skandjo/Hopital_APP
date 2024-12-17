import tkinter as tk
from tkinter import messagebox, ttk
import tools
import psycopg2

class Window_patient :
    """ class pour gerer la fenetre patient"""
    def __init__(self, p_root, db_connection ):
        self.root = p_root

        #conexion a la BD
        self.conn = db_connection  # Réutilise la connexion existante
        self.cursor = self.conn.cursor()  # Réutilise le curseur existant 


    def open_window(self):
        # Méthode générique pour ouvrir une fenêtre de gestion d'une entité donnée (Patients, Médecins, etc.).
        
        window = tk.Toplevel(self.root)  # Crée une nouvelle fenêtre fille (Toplevel).
        window.title(f"Gestion des Patient")  # Définit le titre de la fenêtre.
        window.geometry("600x400")  # Définit les dimensions de la fenêtre.

        # Ajoute un label en haut de la fenêtre avec le nom de l'entité.
        tk.Label(window, text=f"Gestion des patients", font=("Arial", 14)).pack(pady=10)

        # Bouton pour ajouter un nouveau patient.
        tk.Button(window, text=f"Ajouter un patient", font=("Arial", 12), command = self.add).pack(pady=5)

        # Bouton pour afficher la liste des entités (Patients ou Médecins).
        tk.Button(window, text=f"Afficher la Liste des patients", font=("Arial", 12), command = self.list).pack(pady=5)

        # Bouton pour modifier une entité (Patient ou Médecin).
        tk.Button(window, text=f"Modifier un patient", font=("Arial", 12), command = self.modify).pack(pady=5)

        # Bouton pour supprimer une entité (Patient ou Médecin).
        tk.Button(window, text=f"Supprimer un patient", font=("Arial", 12), command = self.delete).pack(pady=5)

        # Bouton pour rechercher une entité (Patient ou Médecin).
        tk.Button(window, text=f"Rechercher un patient", font=("Arial", 12), command = self.search).pack(pady=5)



    def add(self):

        """ Fonction pour ajouter un patient dans la base de données """
        query = "INSERT INTO patients (nom, prenom, date_naissance, sexe, adresse, telephone, email, num_securite_social, contact_urgence_nom, contact_urgence_telephone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
        
        # Création de la fenêtre pour ajouter une entité
        add_window = tk.Toplevel(self.root)
        add_window.title("Ajouter un patient")
        add_window.geometry("400x400")

        # Créer une fenêtre défilable et récupérer la fonction de nettoyage
        scrollable_frame, _ = tools.create_scrollable_window(add_window)

        # Liste des champs
        fields = []
        labels = ["Nom", "Prénom", "Date de naissance (AAAA-MM-JJ)", "Sexe (M/F)",
                "Adresse", "Téléphone", "Email", "Numéro Sécurité Sociale",
                "Contact Urgence Nom", "Contact Urgence Téléphone"]
        optional_fields = ["Contact Urgence Nom", "Contact Urgence Téléphone", "Email"]

        for label in labels:
            tk.Label(scrollable_frame, text=label, font=("Arial", 12)).pack(pady=5)
            entry = tk.Entry(scrollable_frame, font=("Arial", 12))
            entry.pack(pady=5)
            fields.append((label, entry))

        def save_entity():
            missing_fields = []  # Liste des champs obligatoires manquants
            values = []  # Liste des valeurs saisies

            # Vérification des champs saisis
            for label, field in fields:
                value = field.get()  # Récupérer la valeur saisie
                if not value and label not in optional_fields:  # Vérifier les champs obligatoires
                    missing_fields.append(label)  # Ajouter aux champs manquants
                values.append(value)  # Ajouter la valeur à la liste

            # Afficher une erreur si des champs obligatoires sont manquants
            if missing_fields:
                print(missing_fields)
                messagebox.showerror("Champs manquants", f"Les champs suivants sont obligatoires et doivent être remplis :\n{', '.join(missing_fields)}")
                return

            # Insérer les données dans la base de données
            try:
                self.cursor.execute(query, values)  # Exécuter la requête SQL avec les valeurs saisies
                self.conn.commit()  # Confirmer la transaction
                messagebox.showinfo("Succès", "Ajout d'un patient réussi avec succès !")  # Message de confirmation
                add_window.destroy()  # Fermer la fenêtre après succès
            except Exception as e:
                # Afficher une erreur si l'insertion échoue
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        def close_window():
            """Nettoyer les ressources avant de fermer."""
            add_window.destroy()  # Fermer la fenêtre

        # Associer la fermeture propre à la fenêtre
        add_window.protocol("WM_DELETE_WINDOW", close_window)
        tk.Button(scrollable_frame, text="Enregistrer", font=("Arial", 12), command=save_entity).pack(pady=20)


    def list(self):  
        """ Affiche une fenêtre listant les données de la table patients. """

        query = "SELECT * FROM patients"  # La requête

        # Créer une nouvelle fenêtre pour afficher la liste
        list_window = tk.Toplevel(self.root)
        list_window.title("Liste des patients")
        list_window.bind("<Escape>", lambda e: list_window.attributes('-fullscreen', False))

        tk.Label(list_window, text="Liste des Patients", font=("Arial", 14)).pack(pady=10)

        # Récupérer la structure des colonnes dynamiquement
        try:
            self.cursor.execute("SELECT * FROM patients LIMIT 0")  # Utilisé pour récupérer les colonnes
            column_names = [desc[0] for desc in self.cursor.description]
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les colonnes : {e}")
            return

        # Créer un cadre pour contenir Treeview et Scrollbar
        frame = tk.Frame(list_window)
        frame.pack(fill=tk.BOTH, expand=True)

        # Création de la barre de défilement verticale
        scrollbar_list = tk.Scrollbar(frame, orient="vertical")

        # Création du tableau Treeview avec des colonnes dynamiques
        tree = ttk.Treeview(frame, columns=column_names, show="headings", yscrollcommand=scrollbar_list.set)

        # Configurer la Scrollbar pour contrôler le Treeview
        scrollbar_list.config(command=tree.yview)
        scrollbar_list.pack(side=tk.RIGHT, fill=tk.Y)

        # Définir les en-têtes de colonnes
        for col in column_names:
            tree.heading(col, text=col.capitalize())  # Mettre les noms de colonnes en majuscule
            tree.column(col, width=100, anchor="center")  # Ajuster la largeur par défaut

        # Placer le Treeview dans le cadre
        tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Récupérer et insérer les données
        try:
            self.cursor.execute(query)  # Exécuter la requête pour récupérer les données
            for row in self.cursor.fetchall():
                tree.insert("", tk.END, values=row)  # Ajouter chaque ligne au tableau
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des données : {e}")


    def modify(self):
        pass

    def search(self):
        pass

    def delete(self):
        pass