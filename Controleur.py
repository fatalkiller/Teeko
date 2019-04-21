from tkinter import *
from VueJeu import *
from Model import *

class Controleur:
    """ Classe qui gère le passage du menu au jeu et qui gère les différentes actions (clic)
    - root : fenêtre principal de l'application
    - frame : frame contenant les éléements graphiques
    - choix1 / choix2 : contient le type de joueur sélectionner (0 -> joueur, 1 -> IA)
    - model : contient les informations a propos de la partie en cours
    - vueJeu : contient l'interface graphique de la partie en cours
    """

    def __init__(self):
        self.root = Tk()
        self.root.title("Teeko")
        self.root.resizable(0, 0)
        self.root.geometry("500x500")
        self.frame = Frame(self.root, width=500, height=500, borderwidth=1)
        self.creationBarreMenu()
        self.creationMenu()
        self.root.mainloop()

    def creationMenu(self):
        # TODO : modifié le menu (agencement + liste de niveau d'IA)
        self.frame.pack(fill=BOTH)
        self.choix1 = IntVar()
        choix_joueur1 = Radiobutton(self.frame, text="Joueur", variable=self.choix1, value=0)
        choix_ia1 = Radiobutton(self.frame, text="IA", variable=self.choix1, value=1)
        choix_joueur1.pack()
        choix_ia1.pack()
        self.choix2 = IntVar()
        choix_joueur2 = Radiobutton(self.frame, text="Joueur", variable=self.choix2, value=0)
        choix_ia2 = Radiobutton(self.frame, text="IA", variable=self.choix2, value=1)
        choix_joueur2.pack()
        choix_ia2.pack()
        bouton_jouer = Button(self.frame, text="Jouer", command=self.lancementJeu)
        bouton_jouer.pack()

    def actionOnMouseEvent(self, event):
        if not self.model.getGagnant():
            x = event.x - 60
            y = event.y - 60
            # TODO : vérifier si le clic est bien dans le cercle
            if x > 0 and y > 0:
                x = int(x / 82)
                y = int(y / 82)
                if x < 5 and y < 5:
                    if self.model.action(x, y):
                        self.vueJeu.affichage()
                        if self.model.getGagnant():
                            self.afficheGagnant()

    def afficheGagnant(self):
        self.fenetre_gagnant = Tk()
        self.fenetre_gagnant.title('Fin partie')
        self.fenetre_gagnant.geometry("200x100")
        champ_label = Label(self.fenetre_gagnant, text="Le joueur n°" + str(self.model.getTour()) + " a gagné !")
        champ_label.pack()
        self.fenetre_gagnant.mainloop()

    def relanceMenu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.creationMenu()

    def lancementJeu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.model = Model(self.choix1.get(), self.choix2.get())
        self.vueJeu = VueJeu(self.model, self.frame, self.actionOnMouseEvent)

    def creationBarreMenu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Menu", command=self.relanceMenu)

