import tkinter as tk
from tkinter import messagebox, ttk
from Patient import Window_patient
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

        # LES DIFFRENCTE FENETRE ET CLASSE:
        self.patient = Window_patient(self.root, self.conn)
        
        # Création du menu principal après une connexion réussie.
        self.create_main_menu()


    def create_main_menu(self):
        tk.Label(self.root, text="Bienvenue dans l'application de gestion hospitalière", font=("Arial", 16), pady=20).pack()

        # bouton GESTION PATIENT
        tk.Button(self.root, text="Gestion des Patients", font=("Arial", 12), width=30, command=self.patient.open_window).pack(pady=10)

        # bouton QUITTER
        tk.Button(self.root, text="Quitter", font=("Arial", 12), width=30, command=self.close_application).pack(pady=10)


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

