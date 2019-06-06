# -*- coding: utf-8 -*-
from VueJeu import *
from Model import *
from random import randint
import MinMax
import AlphaBeta
import threading
import os
import parameters


class Controleur:
    """ Classe qui gère le passage du menu au jeu et qui gère les différentes actions (clic)
    - root : fenêtre principal de l'application
    - frame : frame contenant les éléments graphiques
    - choix1 / choix2 : contient le type de joueur sélectionner (0 -> joueur, 1 -> IA)
    - model : contient les informations a propos de la partie en cours
    - vueJeu : contient l'interface graphique de la partie en cours
    """

    enable_click = True

    def __init__(self):
        self.root = Tk()
        self.root.title("Teeko")
        self.root.resizable(0, 0)
        self.root.geometry("500x500")
        self.frame = Frame(self.root, width=500, height=500, borderwidth=1)
        self.creation_barre_menu()
        self.creation_menu()
        self.root.mainloop()

    def creation_menu(self):
        # TODO : modifié le menu (agencement + liste de niveau d'IA)
        self.frame.pack(fill=BOTH)
        self.choix_1 = IntVar()
        self.choix_2 = IntVar()
        choix_joueur1 = Radiobutton(
            self.frame, text="Joueur", variable=self.choix_1, value=0)
        choix_ia1 = Radiobutton(self.frame, text="IA",
                                variable=self.choix_1, value=1)
        choix_joueur1.pack()
        choix_ia1.pack()
        choix_joueur2 = Radiobutton(
            self.frame, text="Joueur", variable=self.choix_2, value=0)
        choix_ia2 = Radiobutton(self.frame, text="IA",
                                variable=self.choix_2, value=1)
        choix_joueur2.pack()
        choix_ia2.pack()
        bouton_jouer = Button(self.frame, text="Jouer",
                              command=self.lancement_jeu)
        bouton_jouer.pack()

    def action_on_mouse_event(self, event):
        if not self.model.get_gagnant() and self.enable_click:
            x = event.x - 60
            y = event.y - 60
            if x > 0 and y > 0:
                x = int(x / 82)
                y = int(y / 82)
                if x < 5 and y < 5:
                    if self.model.action(x, y):
                        # Affiche le coup du joueur courant
                        self.vue_jeu.affichage()

                        # Si c'est au tour de l'ia de jouer
                        if self.model.tour == self.model.joueur1 == self.model.TYPE_IA or (self.model.tour == 2 and self.model.joueur2 == self.model.TYPE_IA):
                            # Désactive click utilisateur pendant que l'ia joue
                            self.enable_click = False

                            if parameters.elagage:
                                functarget = AlphaBeta.min_max

                            else:
                                functarget = MinMax.min_max

                            # Lance calcul de l'ia dans un thread
                            t = threading.Thread(
                                target=functarget, args=(self.model, parameters.pMax))
                            t.start()

                            # Attendre que l'IA joue...
                            t.join()

                        self.vue_jeu.affichage()
                        self.enable_click = True

                        if self.model.get_gagnant():
                            self.affiche_gagnant()

    def ia_vs_ia(self):
        # Pose un premier pion aléatoirement
        x = randint(0, 4)
        y = randint(0, 4)
        self.model.pose_pion(x, y)

        # Joue tant qu'il n'y a pas de gagnant
        while not self.model.gagnant:
            if parameters.elagage:
                functarget = AlphaBeta.min_max

            else:
                functarget = MinMax.min_max

            # Lance calcul de l'ia dans un thread
            t = threading.Thread(
                target=functarget, args=(self.model, parameters.pMax))
            t.start()

            # Attendre que l'IA joue...
            t.join()

            self.vue_jeu.affichage()

    def affiche_gagnant(self):
        self.fenetre_gagnant = Tk()
        self.fenetre_gagnant.title('Fin partie')
        self.fenetre_gagnant.geometry("200x100")
        champ_label = Label(self.fenetre_gagnant, text="Le joueur n°" +
                                                       str(self.model.get_tour()) + " a gagné !")
        champ_label.pack()
        self.fenetre_gagnant.mainloop()

    def relance_menu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.creation_menu()

    def lancement_jeu(self):
        for widget in self.frame.winfo_children():
            widget.destroy()
        self.model = Model(self.choix_1.get(), self.choix_2.get())
        # Si combat IA vs IA, alors lancer le jeu dans une console
        if self.model.joueur1 == self.model.joueur2 == self.model.TYPE_IA:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            # os.path.join(dir_path, 'VueConsole.py')
            os.system('start /B start cmd.exe @cmd /k python ' +
                      dir_path + "\VueConsole.py")
            # self.iAvsIA()
        # Sinon, lancer le GUI du jeu
        else:
            self.vue_jeu = VueJeu(self.model, self.frame,
                                  self.action_on_mouse_event)

    def creation_barre_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Rejouer", command=self.relance_menu)
