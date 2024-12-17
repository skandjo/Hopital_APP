import tkinter as tk
from tkinter import messagebox, ttk
import psycopg2

class HospitalApp:
    def __init__(self, p_root, p_dbname, p_user, p_password):
        # Initialisation de l'application avec les paramètres fournis.
        self.root = p_root
        self.root.title("Gestion des données hospitalières")  # Définition du titre de la fenêtre principale.
        self.root.geometry("800x600")  # Définition de la taille de la fenêtre principale.

        try:
            # Connexion à la base de données PostgreSQL avec les informations fournies.
            self.conn = psycopg2.connect(
                dbname=p_dbname,
                user=p_user,
                password=p_password,
                host="localhost",  # Hôte de la base de données, ici 'localhost'.
                port="5432"  # Port par défaut pour PostgreSQL.
            )
            self.cursor = self.conn.cursor()  # Création d'un curseur pour exécuter des requêtes SQL.
        except Exception as e:
            # Gestion des erreurs de connexion.
            messagebox.showerror("Erreur de connexion", f"Impossible de se connecter à la base de données : {e}")
            self.root.destroy()  # Ferme l'application en cas d'échec de connexion.
            return

        # Création du menu principal après une connexion réussie.
        self.create_main_menu()

    def create_main_menu(self):
        tk.Label(self.root, text="Bienvenue dans l'application de gestion hospitalière",
                 font=("Arial", 16), pady=20).pack()

        tk.Button(self.root, text="Gestion des Patients", font=("Arial", 12),
                  width=30, command=self.open_patient_window).pack(pady=10)

        tk.Button(self.root, text="Gestion des Médecins", font=("Arial", 12),
                  width=30, command=self.open_medecin_window).pack(pady=10)

        tk.Button(self.root, text="Gestion des Départements", font=("Arial", 12),
                  width=30, command=self.open_department_window).pack(pady=10)

        tk.Button(self.root, text="Gestion des Chambres", font=("Arial", 12),
                  width=30, command=self.open_room_window).pack(pady=10)

        tk.Button(self.root, text="Gestion des Consultations", font=("Arial", 12),
                  width=30, command=self.open_consultation_window).pack(pady=10)

        tk.Button(self.root, text="Gestion des Hospitalisations", font=("Arial", 12),
                  width=30, command=self.open_hospitalization_window).pack(pady=10)

        tk.Button(self.root, text="Quitter", font=("Arial", 12), width=30,
                  command=self.close_application).pack(pady=10)


    def open_patient_window(self):
        # Méthode pour ouvrir une fenêtre dédiée à la gestion des patients.
        # Utilise la méthode générique `open_entity_window` avec les callbacks spécifiques aux patients.
        self.open_entity_window(
            "Patients",  # Nom de l'entité à gérer.
            self.add_patient,  # Fonction pour ajouter un patient.
            self.list_patients,  # Fonction pour lister les patients.
            self.modify_patient,  # Fonction pour modifier un patient.
            self.delete_patient,  # Fonction pour supprimer un patient.
            self.search_patient   # Fonction pour rechercher un patient.
        )

    def open_medecin_window(self):
        # Méthode pour ouvrir une fenêtre dédiée à la gestion des médecins.
        # Utilise la méthode générique `open_entity_window` avec les callbacks spécifiques aux médecins.
        self.open_entity_window(
            "Médecins",  # Nom de l'entité à gérer.
            self.add_medecin,  # Fonction pour ajouter un médecin.
            self.list_medecins,  # Fonction pour lister les médecins.
            self.modify_medecin,  # Fonction pour modifier un médecin.
            self.delete_medecin,  # Fonction pour supprimer un médecin.
            self.search_medecin   # Fonction pour rechercher un médecin.
        )

    def open_department_window(self):
        self.open_entity_window(
            "Départements", self.add_department, self.list_departments,
            self.modify_department, self.delete_department, None
        )

    def open_room_window(self):
        self.open_entity_window(
            "Chambres", self.add_room, self.list_rooms, self.modify_room, self.delete_room, None
        )

    def open_consultation_window(self):
        self.open_entity_window(
            "Consultations", self.add_consultation, self.list_consultations,
            self.modify_consultation, self.delete_consultation, None
        )

    def open_hospitalization_window(self):
        self.open_entity_window(
            "Hospitalisations", self.add_hospitalization, self.list_hospitalizations,
            self.modify_hospitalization, self.delete_hospitalization, None
        )

    def open_entity_window(self, entity_name, add_callback, list_callback, modify_callback, delete_callback, search_callback):
        # Méthode générique pour ouvrir une fenêtre de gestion d'une entité donnée (Patients, Médecins, etc.).
        
        window = tk.Toplevel(self.root)  # Crée une nouvelle fenêtre fille (Toplevel).
        window.title(f"Gestion des {entity_name}")  # Définit le titre de la fenêtre.
        window.geometry("600x400")  # Définit les dimensions de la fenêtre.

        # Ajoute un label en haut de la fenêtre avec le nom de l'entité.
        tk.Label(window, text=f"Gestion des {entity_name}", font=("Arial", 14)).pack(pady=10)

        # Bouton pour ajouter une nouvelle entité (Patient ou Médecin).
        tk.Button(window, text=f"Ajouter un {entity_name[:-1]}", font=("Arial", 12),
                command=add_callback).pack(pady=5)

        # Bouton pour afficher la liste des entités (Patients ou Médecins).
        tk.Button(window, text=f"Afficher la Liste des {entity_name}", font=("Arial", 12),
                command=list_callback).pack(pady=5)

        # Bouton pour modifier une entité (Patient ou Médecin).
        tk.Button(window, text=f"Modifier un {entity_name[:-1]}", font=("Arial", 12),
                command=modify_callback).pack(pady=5)

        # Bouton pour supprimer une entité (Patient ou Médecin).
        tk.Button(window, text=f"Supprimer un {entity_name[:-1]}", font=("Arial", 12),
                command=delete_callback).pack(pady=5)

        # Bouton pour rechercher une entité (Patient ou Médecin).
        tk.Button(window, text=f"Rechercher un {entity_name[:-1]}", font=("Arial", 12),
                command=search_callback).pack(pady=5)


    def add_patient(self):
        """
        Cette méthode utilise la méthode générique `add_entity` pour créer une interface graphique.
        La requête SQL correspond à l'insertion dans la table 'patients'.
        """
        self.add_entity("Ajouter un Patient",  # Titre de la fenêtre
            "INSERT INTO patients (nom, prenom, date_naissance, sexe, adresse, telephone, email, num_securite_social, contact_urgence_nom, contact_urgence_telephone) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  # Requête SQL
        )

    def add_medecin(self):
        
        self.add_entity("Ajouter un Médecin", "INSERT INTO medecins (nom, prenom, date_naissance, sexe, adresse, telephone, email, specialite, salaire, date_embauche, etat) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"  )
    def add_department(self):
        self.add_entity("Ajouter un Département", "INSERT INTO departements (nom, description, telephone, chef_id) VALUES (%s, %s, %s, %s)")

    def add_room(self):
        self.add_entity("Ajouter une Chambre", "INSERT INTO chambres (num_chambre, departement_id, disponibilite) VALUES (%s, %s, %s)")

    def add_consultation(self):
        self.add_entity("Ajouter une Consultation", "INSERT INTO consultations (patient_id, medecin_id, date_consultation, diagnostic, traitement_prescrit) VALUES (%s, %s, %s, %s, %s)")

    def add_hospitalization(self):
        self.add_entity("Ajouter une Hospitalisation", "INSERT INTO hospitalisation (patient_id, chambre_id, date_hospitalisation, diagnostic, traitement_prescrit) VALUES (%s, %s, %s, %s, %s)")

    
    def add_entity(self, title, query):
        """
        Ouvre une fenêtre pour ajouter une entité (Patient ou Médecin).
        
        Args:
            title (str): Le titre de la fenêtre (par exemple, "Ajouter un Patient").
            query (str): Requête SQL pour insérer les données dans la base de données.
        """
        # Création de la fenêtre pour ajouter une entité
        add_window = tk.Toplevel(self.root)
        add_window.title(title)  # Définir le titre de la fenêtre
        add_window.geometry("400x400")  # Définir les dimensions de la fenêtre

        # Création du canvas_add pour permettre le défilement vertical
        canvas_add = tk.Canvas(add_window)
        scrollbar = tk.Scrollbar(add_window, orient="vertical", command=canvas_add.yview)
        scrollable_frame = tk.Frame(canvas_add)

        # Configurer le canvas_add pour qu'il s'adapte à la taille du contenu
        scrollable_frame.bind("<Configure>", lambda e: canvas_add.configure(scrollregion=canvas_add.bbox("all")))

        # Fonctionnalité de défilement avec la molette de la souris
        def on_mouse_wheel(event):
            canvas_add.yview_scroll(-1 * (event.delta // 120), "units")

        # Lier les événements de défilement 
        canvas_add.bind_all("<MouseWheel>", on_mouse_wheel)  # Défilement
        canvas_add.bind_all("<Button-4>", lambda e: canvas_add.yview_scroll(-1, "units"))  # Défilement (haut) 
        canvas_add.bind_all("<Button-5>", lambda e: canvas_add.yview_scroll(1, "units"))  # Défilement (bas) 

        # Configuration du canvas_add pour contenir le contenu scrollable
        canvas_add.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_add.configure(yscrollcommand=scrollbar.set)

        # Placement des widgets canvas_add et scrollbar dans la fenêtre
        canvas_add.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Liste pour stocker les champs de saisie
        fields = []

        # Définition des labels et champs en fonction du type d'entité
        if "Patient" in title:
            labels = [
                "Nom", "Prénom", "Date de naissance (AAAA-MM-JJ)", "Sexe (M/F)", 
                "Adresse", "Téléphone", "Email", "Numéro Sécurité Sociale", 
                "Contact Urgence Nom", "Contact Urgence Téléphone"
            ]
        elif "Médecin" in title:
            labels = [
                "Nom", "Prénom", "Date de naissance (AAAA-MM-JJ)", "Sexe (M/F)", 
                "Adresse", "Téléphone", "Email", "Spécialité", "Salaire", 
                "Date d'embauche (AAAA-MM-JJ)", "État (actif/congés)"
            ]

        # Champs facultatifs, non obligatoires pour validation
        optional_fields = ["Contact Urgence Nom", "Contact Urgence Téléphone", "Email"]

        # Création des labels et champs de saisie pour chaque attribut
        for label in labels:
            tk.Label(scrollable_frame, text=label, font=("Arial", 12)).pack(pady=5)  # Ajouter un label
            entry = tk.Entry(scrollable_frame, font=("Arial", 12))  # Ajouter une zone de saisie
            entry.pack(pady=5)
            fields.append((label, entry))  # Associer le label au champ pour validation

        # Fonction pour sauvegarder les données saisies
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
                messagebox.showinfo("Succès", f"{title} réussi avec succès !")  # Message de confirmation
                add_window.destroy()  # Fermer la fenêtre après succès
            except Exception as e:
                # Afficher une erreur si l'insertion échoue
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        # Bouton pour enregistrer l'entité dans la base de données
        tk.Button(scrollable_frame, text="Enregistrer", font=("Arial", 12),
                command=save_entity).pack(pady=20)



    def list_patients(self):
        self.list_entities("Patients", "SELECT * FROM patients")

    def list_medecins(self):
        self.list_entities("Medecins", "SELECT * FROM medecins")

    def list_departments(self):
        self.list_entities("Départements", "SELECT * FROM departements")

    def list_rooms(self):
        self.list_entities("Chambres", "SELECT * FROM chambres")

    def list_consultations(self):
        self.list_entities("Consultations", "SELECT * FROM consultations")

    def list_hospitalizations(self):
        self.list_entities("Hospitalisations", "SELECT * FROM hospitalisation")

    def list_entities(self, entity_name, query):
        """
        Affiche une fenêtre listant les données d'une table donnée.

        Args:
            entity_name (str): Nom de l'entité à afficher ('Patients' ou 'Médecins').
            query (str): Requête SQL pour récupérer les données de la table.
        """
        # Créer une nouvelle fenêtre pour afficher la liste
        list_window = tk.Toplevel(self.root)
        list_window.title(f"Liste des {entity_name}")
        list_window.bind("<Escape>", lambda e: list_window.attributes('-fullscreen', False))

        tk.Label(list_window, text=f"Liste des {entity_name}", font=("Arial", 14)).pack(pady=10)

        # Récupérer la structure des colonnes dynamiquement
        try:
            self.cursor.execute(f"SELECT * FROM {entity_name.lower()} LIMIT 0")  # Utilisé pour récupérer les colonnes
            column_names = [desc[0] for desc in self.cursor.description]
        except Exception as e:
            messagebox.showerror("Erreur", f"Impossible de récupérer les colonnes : {e}")
            return

        # Création du tableau Treeview avec des colonnes dynamiques
        tree = ttk.Treeview(list_window, columns=column_names, show="headings")

        # Définir les en-têtes de colonnes
        for col in column_names:
            tree.heading(col, text=col.capitalize())  # Mettre les noms de colonnes en majuscule
            tree.column(col, width=100, anchor="center")  # Ajuster la largeur par défaut

        tree.pack(fill=tk.BOTH, expand=True)

        # Récupérer et insérer les données
        try:
            self.cursor.execute(query)  # Exécuter la requête pour récupérer les données
            for row in self.cursor.fetchall():
                tree.insert("", tk.END, values=row)  # Ajouter chaque ligne au tableau
        except Exception as e:
            messagebox.showerror("Erreur", f"Une erreur s'est produite lors de la récupération des données : {e}")




    def modify_patient(self):
        """Méthode pour modifier les informations d'un patient."""
        self.modify_entity("Modifier un Patient")

    def modify_medecin(self):
        """Méthode pour modifier les informations d'un médecin."""
        self.modify_entity("Modifier un Médecin")

    def modify_department(self):
        self.modify_entity("Modifier un Département")

    def modify_room(self):
        self.modify_entity("Modifier une Chambre")

    def modify_consultation(self):
        self.modify_entity("Modifier une Consultation")

    def modify_hospitalization(self):
        self.modify_entity("Modifier une Hospitalisation")

    def modify_entity(self, title):
        """
        Méthode générique pour modifier une entité (patient ou médecin).
        :param title: Le titre de la fenêtre ("Modifier un Patient" ou "Modifier un Médecin").
        """
        modify_window = tk.Toplevel(self.root)
        modify_window.title(title)
        modify_window.geometry("500x500")

        # Création d'un canvas_modify avec une barre de défilement
        canvas_modify = tk.Canvas(modify_window, width=480, height=680)
        scrollbar = ttk.Scrollbar(modify_window, orient="vertical", command=canvas_modify.yview)
        scrollable_frame = tk.Frame(canvas_modify)

        # Synchroniser le canvas_modify avec le contenu dynamique
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas_modify.configure(scrollregion=canvas_modify.bbox("all"))
        )

        canvas_modify.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas_modify.configure(yscrollcommand=scrollbar.set)

        canvas_modify.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Choix de l'attribut d'identification
        tk.Label(scrollable_frame, text="Attribut pour identifier l'entité", font=("Arial", 12)).pack(pady=5)
        search_attribute_combobox = ttk.Combobox(scrollable_frame, state="readonly", font=("Arial", 12))
        search_attributes = ["id", "nom", "prenom", "num_securite_social"]
        search_attribute_combobox['values'] = search_attributes
        search_attribute_combobox.current(0)
        search_attribute_combobox.pack(pady=5)

        # Saisie de la valeur de l'attribut d'identification
        tk.Label(scrollable_frame, text="Valeur de l'attribut d'identification", font=("Arial", 12)).pack(pady=5)
        search_value_entry = tk.Entry(scrollable_frame, font=("Arial", 12))
        search_value_entry.pack(pady=5)

        # Instructions pour sélectionner les attributs à modifier
        tk.Label(scrollable_frame, text="Sélectionnez les attributs à modifier", font=("Arial", 12)).pack(pady=10)

        # Définir les attributs en fonction de l'entité (Patient ou Médecin)
        if "Patient" in title:
            attributes = ["id", "nom", "prenom", "date_naissance", "sexe", "adresse", "telephone", "email", "num_securite_social", "contact_urgence_nom", "contact_urgence_telephone"]
        elif "Médecin" in title:
            attributes = ["id", "nom", "prenom", "date_naissance", "sexe", "adresse", "telephone", "email", "specialite", "salaire", "date_embauche", "etat"]

        fields = []
        checkboxes = []
        for attribute in attributes:
            # Création de cases à cocher pour chaque attribut
            var = tk.BooleanVar()
            checkbox = tk.Checkbutton(scrollable_frame, text=attribute, variable=var, font=("Arial", 12))
            checkbox.pack(anchor="w", padx=10)
            entry = tk.Entry(scrollable_frame, font=("Arial", 12))
            entry.pack(pady=5)
            checkboxes.append((attribute, var))
            fields.append(entry)

        def update_entity():
            """Met à jour l'entité dans la base de données."""
            search_attribute = search_attribute_combobox.get()
            search_value = search_value_entry.get()

            if not search_value:
                messagebox.showerror("Erreur", "Veuillez remplir l'attribut d'identification.")
                return

            # Préparer les colonnes et valeurs à modifier
            updates = []
            values = []
            for i, (attribute, var) in enumerate(checkboxes):
                if var.get():  # Vérifie si l'attribut est sélectionné
                    new_value = fields[i].get()
                    if new_value:
                        updates.append(f"{attribute}=%s")
                        values.append(new_value)

            if not updates:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins un attribut à modifier.")
                return

            # Ajouter la valeur de l'attribut de recherche
            values.append(search_value)

            # Générer la requête SQL dynamique
            table = "patients" if "Patient" in title else "medecins"
            dynamic_query = f"UPDATE {table} SET {', '.join(updates)} WHERE {search_attribute}=%s"

            try:
                self.cursor.execute(dynamic_query, values)
                self.conn.commit()
                messagebox.showinfo("Succès", f"{title.split(' ')[-1]} modifié(e) avec succès !")
                modify_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        # Bouton pour soumettre les modifications
        tk.Button(scrollable_frame, text="Modifier", font=("Arial", 12),
                command=update_entity).pack(pady=20)


    def delete_patient(self):
        self.delete_entity("Supprimer un Patient", "DELETE FROM patients WHERE id=%s")

    def delete_medecin(self):
        self.delete_entity("Supprimer un Médecin", "DELETE FROM medecins WHERE id=%s")
    def delete_department(self):
        self.delete_entity("Supprimer un Département", "DELETE FROM departements WHERE id=%s")

    def delete_room(self):
        self.delete_entity("Supprimer une Chambre", "DELETE FROM chambres WHERE id=%s")

    def delete_consultation(self):
        self.delete_entity("Supprimer une Consultation", "DELETE FROM consultations WHERE id=%s")

    def delete_hospitalization(self):
        self.delete_entity("Supprimer une Hospitalisation", "DELETE FROM hospitalisation WHERE id=%s")

    def delete_entity(self, title, query):
        delete_window = tk.Toplevel(self.root)
        delete_window.title(title)
        delete_window.geometry("300x200")

        tk.Label(delete_window, text="ID de l'entité à supprimer", font=("Arial", 12)).pack(pady=5)
        id_entry = tk.Entry(delete_window, font=("Arial", 12))
        id_entry.pack(pady=5)

        def execute_delete():
            entity_id = id_entry.get()
            try:
                self.cursor.execute(query, (entity_id,))
                self.conn.commit()
                messagebox.showinfo("Succès", f"{title} réussi avec succès !")
                delete_window.destroy()
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        tk.Button(delete_window, text="Supprimer", font=("Arial", 12),
                  command=execute_delete).pack(pady=20)

    def search_patient(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Recherche d'un Patient")
        search_window.geometry("400x400")

        # Création d'un canvas_search pour contenir tout le contenu et permettre le défilement
        canvas_search = tk.Canvas(search_window)
        canvas_search.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Ajout d'une scrollbar verticale associée au canvas_search
        scrollbar = tk.Scrollbar(search_window, orient=tk.VERTICAL, command=canvas_search.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas_search.configure(yscrollcommand=scrollbar.set)

        # Frame à l'intérieur du canvas_search pour contenir les widgets
        content_frame = tk.Frame(canvas_search)

        # Création d'un "window" dans le canvas_search pour contenir le frame
        canvas_search.create_window((0, 0), window=content_frame, anchor="nw")

        # Assurer que le canvas_search s'ajuste à la taille du frame
        def on_configure(event):
            canvas_search.configure(scrollregion=canvas_search.bbox("all"))

        content_frame.bind("<Configure>", on_configure)

        # Contenu de la fenêtre
        tk.Label(content_frame, text="Rechercher un patient par :", font=("Arial", 12)).pack(pady=5)

        search_type = ttk.Combobox(content_frame, state="readonly", font=("Arial", 12))
        search_type['values'] = ["Nom", "Numéro Sécurité Sociale"]
        search_type.current(0)
        search_type.pack(pady=5)

        tk.Label(content_frame, text="Valeur de recherche :", font=("Arial", 12)).pack(pady=5)
        search_value = tk.Entry(content_frame, font=("Arial", 12))
        search_value.pack(pady=5)

        tk.Label(content_frame, text="Choisir les attributs à afficher :", font=("Arial", 12)).pack(pady=5)

        # Liste des attributs des patients
        patient_attributes = [
            "id", "nom", "date_naissance", "sexe", "adresse", 
            "telephone", "email", "num_securite_social", 
            "contact_urgence_nom", "contact_urgence_telephone"
        ]

        # Ajout d'une zone de sélection multiple
        selected_attributes = []
        for attr in patient_attributes:
            var = tk.BooleanVar(value=False)
            checkbox = tk.Checkbutton(content_frame, text=attr, variable=var)
            checkbox.pack(anchor="w")
            selected_attributes.append((attr, var))

        def perform_search():
            search_criteria = search_type.get()
            value = search_value.get()

            if not value:
                messagebox.showerror("Erreur", "Veuillez entrer une valeur de recherche.")
                return

            # Construire la requête SQL pour les attributs sélectionnés
            chosen_attributes = [attr for attr, var in selected_attributes if var.get()]
            if not chosen_attributes:
                messagebox.showerror("Erreur", "Veuillez sélectionner au moins un attribut à afficher.")
                return

            selected_columns = ", ".join(chosen_attributes)
            if search_criteria == "Nom":
                query = f"SELECT {selected_columns} FROM patients WHERE nom = %s"
                params = (value,)
            elif search_criteria == "Numéro Sécurité Sociale":
                query = f"SELECT {selected_columns} FROM patients WHERE num_securite_social = %s"
                params = (value,)

            try:
                self.cursor.execute(query, params)
                results = self.cursor.fetchall()
                if results:
                    self.display_results("Patients", results, chosen_attributes)
                else:
                    messagebox.showinfo("Résultats", "Aucun patient trouvé.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        tk.Button(content_frame, text="Rechercher", font=("Arial", 12),
                command=perform_search).pack(pady=10)

        # Rendre le canvas_search défilable avec la molette de la souris
        def on_mousewheel(event):
            canvas_search.yview_scroll(-1 * int(event.delta / 120), "units")

        canvas_search.bind_all("<MouseWheel>", on_mousewheel)

    def search_medecin(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Recherche d'un Médecin")
        search_window.geometry("400x300")

        tk.Label(search_window, text="Rechercher un médecin par Nom et Prénom", font=("Arial", 12)).pack(pady=5)

        tk.Label(search_window, text="Nom :", font=("Arial", 12)).pack(pady=5)
        name_entry = tk.Entry(search_window, font=("Arial", 12))
        name_entry.pack(pady=5)

        tk.Label(search_window, text="Prénom :", font=("Arial", 12)).pack(pady=5)
        surname_entry = tk.Entry(search_window, font=("Arial", 12))
        surname_entry.pack(pady=5)

        def perform_search():
            name = name_entry.get()
            surname = surname_entry.get()

            if not name or not surname:
                messagebox.showerror("Erreur", "Veuillez entrer le nom et le prénom.")
                return

            query = "SELECT * FROM medecins WHERE nom = %s AND prenom = %s"
            try:
                self.cursor.execute(query, (name, surname))
                results = self.cursor.fetchall()
                if results:
                    self.display_results("Médecins", results)
                else:
                    messagebox.showinfo("Résultats", "Aucun médecin trouvé.")
            except Exception as e:
                messagebox.showerror("Erreur", f"Une erreur s'est produite : {e}")

        tk.Button(search_window, text="Rechercher", font=("Arial", 12),
                  command=perform_search).pack(pady=10)

    def display_results(self, entity_name, results, columns):
        results_window = tk.Toplevel(self.root)
        results_window.title(f"Résultats de la recherche ({entity_name})")
        results_window.geometry("600x400")

        tk.Label(results_window, text=f"Résultats de la recherche ({entity_name})", font=("Arial", 14)).pack(pady=10)

        tree = ttk.Treeview(results_window, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col.capitalize())

        tree.pack(fill=tk.BOTH, expand=True)

        for row in results:
            tree.insert("", tk.END, values=row)



    def close_application(self):
        if messagebox.askokcancel("Quitter", "Êtes-vous sûr de vouloir quitter ?"):
            self.cursor.close()
            self.conn.close()
            self.root.destroy()

# Code pour exécuter l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalApp(root, 'hopital_db', 'postgres', '140600')
    root.mainloop()
