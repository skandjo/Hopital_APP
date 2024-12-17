import tkinter as tk
from tkinter import messagebox, ttk

def create_scrollable_window(window):
    """Crée un canvas avec barre de défilement et gère les événements proprement."""
    
    # Création du canvas et de la barre de défilement
    canvas = tk.Canvas(window)
    scrollbar = tk.Scrollbar(window, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    # Configuration pour adapter le canvas au contenu
    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    # Défilement avec la molette de la souris (lié uniquement au canvas)
    def on_mouse_wheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind("<MouseWheel>", on_mouse_wheel)
    canvas.bind("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
    canvas.bind("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))

    # Ajouter le cadre défilable au canvas
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Placement des widgets canvas et scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Fonction de nettoyage pour détruire les widgets et détacher les bindings
    def cleanup():
        canvas.unbind("<MouseWheel>")
        canvas.unbind("<Button-4>")
        canvas.unbind("<Button-5>")
        canvas.destroy()
        scrollbar.destroy()

    return scrollable_frame, cleanup

