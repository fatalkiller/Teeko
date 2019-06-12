# -*- coding: utf-8 -*-
from VueJeu import *
from Model import *
from random import randint
import MinMax
import AlphaBeta
import threading
import os


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
        self.frame = Frame(self.root, width=500, height=550, borderwidth=1)
        self.creation_barre_menu()
        self.creation_menu()
        self.root.mainloop()

    def creation_menu(self):
        self.frame.pack(fill=BOTH)

        self.choix_1 = IntVar()
        self.choix_2 = IntVar()

        self.label_1 = Label(self.frame, text="Niveau IA 1 : ")
        self.label_2 = Label(self.frame, text="Niveau IA 2 : ")

        self.lb_1 = Listbox(self.frame, height=len(
            parameters.tabLevels), selectmode=SINGLE, exportselection=0)
        self.lb_2 = Listbox(self.frame, height=len(
            parameters.tabLevels), selectmode=SINGLE, exportselection=0)

        choix_joueur1 = Radiobutton(
            self.frame, text="Joueur", variable=self.choix_1, value=0)
        choix_ia1 = Radiobutton(self.frame, text="IA",
                                variable=self.choix_1, value=1)
        choix_joueur1.pack()
        choix_ia1.pack()

        self.label_1.pack()

        for i in range(1, len(parameters.tabLevels) + 1):
            self.lb_1.insert(END, i)
        self.lb_1.pack()

        choix_joueur2 = Radiobutton(
            self.frame, text="Joueur", variable=self.choix_2, value=0)
        choix_ia2 = Radiobutton(self.frame, text="IA",
                                variable=self.choix_2, value=1)
        choix_joueur2.pack()
        choix_ia2.pack()

        self.label_2.pack()

        for i in range(1, len(parameters.tabLevels) + 1):
            self.lb_2.insert(END, i)
        self.lb_2.pack()

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

                            pMax = self.model.pMax_ias[self.model.tour]
                            eval_enable = self.model.eval_ias[self.model.tour]

                            # Lance calcul de l'ia dans un thread
                            t = threading.Thread(
                                target=functarget, args=(self.model, pMax, eval_enable))
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

            pMax = self.model.pMax_ias[self.model.tour]
            eval_enable = self.model.eval_ias[self.model.tour]

            # Lance calcul de l'ia dans un thread
            t = threading.Thread(
                target=functarget, args=(self.model, pMax, eval_enable))
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
        selection_level_ia_1 = self.lb_1.curselection()
        selection_level_ia_2 = self.lb_2.curselection()

        # Tester si un des joueurs est une IA
        # et si un niveau est bien sélectionné
        ready = True
        if self.choix_1.get() == 1 and not selection_level_ia_1:
            ready = False
        if self.choix_2.get() == 1 and not selection_level_ia_2:
            ready = False

        # Si il y a une IA et que son niveau et sélectionné
        if ready:
            # Création du model
            self.model = Model(self.choix_1.get(), self.choix_2.get())

            # Récupération du niveau de chaque IA (si un des joueur est de type IA au moins)
            # set pMax et eval boolean
            if self.choix_1.get() == 1:
                self.model.pMax_ias[1] = parameters.tabLevels[self.lb_1.get(
                    ACTIVE) - 1][1]
                self.model.eval_ias[1] = parameters.tabLevels[self.lb_1.get(
                    ACTIVE) - 1][2]
            if self.choix_2.get() == 1:
                self.model.pMax_ias[2] = parameters.tabLevels[self.lb_2.get(
                    ACTIVE) - 1][1]
                self.model.eval_ias[2] = parameters.tabLevels[self.lb_2.get(
                    ACTIVE) - 1][2]

            # Si combat IA vs IA, alors lancer le jeu dans une console
            if self.model.joueur1 == self.model.joueur2 == self.model.TYPE_IA:
                dir_path = os.path.dirname(os.path.realpath(__file__))
                # os.path.join(dir_path, 'VueConsole.py')
                pMax_1 = str(
                    parameters.tabLevels[self.lb_1.get(ACTIVE) - 1][1])
                eval_1 = str(
                    parameters.tabLevels[self.lb_1.get(ACTIVE) - 1][2])
                pMax_2 = str(
                    parameters.tabLevels[self.lb_2.get(ACTIVE) - 1][1])
                eval_2 = str(
                    parameters.tabLevels[self.lb_2.get(ACTIVE) - 1][2])

                os.system('start /B start cmd.exe @cmd /k python ' +
                          dir_path + "\VueConsole.py" + " " + pMax_1 + " " + eval_1 + " " + pMax_2 + " " + eval_2)
                # Enleve le menu affiché
                for widget in self.frame.winfo_children():
                    widget.destroy()
            # Sinon, lancer le GUI du jeu
            else:
                # Enleve le menu affiché
                for widget in self.frame.winfo_children():
                    widget.destroy()
                self.vue_jeu = VueJeu(self.model, self.frame,
                                      self.action_on_mouse_event)
                self.vue_jeu.update_status_label()

    def creation_barre_menu(self):
        menubar = Menu(self.root)
        self.root.config(menu=menubar)
        menubar.add_command(label="Rejouer", command=self.relance_menu)
