from Model import *
import MinMax
import AlphaBeta
import parameters
import threading
import sys
from random import randint
from time import sleep


class VueConsole:
    def __init__(self, model):
        self.model = model

    def affiche_plateau(self):
        print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
        affichage = "-------------------------\n" \
            "| / | 0 | 1 | 2 | 3 | 4 |\n" \
            "-------------------------\n"
        for j in range(5):
            affichage += "| " + str(j) + " |"
            for i in range(5):
                sym = " "
                if self.model.plateau[i][j] == 1:
                    sym = "O"
                if self.model.plateau[i][j] == 2:
                    sym = "X"
                affichage += " " + sym + " |"
            affichage += "\n" \
                "-------------------------\n"
        print(affichage)

    def change_tour(self):
        self.model.change_tour()
        self.affiche_plateau()

    def tour_de_jeu(self):
        self.affiche_plateau()
        for i in range(0, 8):
            self.pose_pion()
            self.change_tour()
            if self.model.gagnant:
                break

        while not self.model.gagnant:
            self.deplace_pion()
            self.change_tour()

    def pose_pion(self):
        while True:
            posX = int(
                input('Veuillez rentrez la colonne du pion à posé (entre 0 et 4)  : \n'))
            posY = int(
                input('Veuillez rentrez la ligne du pion à posé (entre 0 et 4)  : \n'))
            if 0 <= posX < 5 and 0 <= posY < 5 and self.model.plateau[posX][posY] == 0:
                self.model.plateau[posX][posY] = self.model.tour
                break
            print('mauvaise position')

    def deplace_pion(self):
        while True:
            posX = int(
                input('Veuillez rentrez la colonne du pion à déplacer (entre 0 et 4)  : \n'))
            posY = int(
                input('Veuillez rentrez la ligne du pion à déplacer (entre 0 et 4)  : \n'))
            if posX < 0 or posX > 4 or posY < 0 or posY > 4:
                print("numéro de ligne est colonne entre 0 et 4 ! \n")
            elif self.model.plateau[posX][posY] == self.model.tour:
                break
            else:
                print("Aucun pion de votre couleur à cette position ! \n")

        self.model.plateau[posX][posY] = 0

        posXA = posX
        posYA = posY
        while True:
            deplacement = int(input(
                'Veuillez rentrez le deplacement du pion (entre 1 et 8 dans le sens des aiguilles d une montre en partant du haut à gauche)  : \n'))
            if deplacement == 1:
                posXA = posX-1
                posYA = posY-1
            elif deplacement == 2:
                posYA = posY-1
            elif deplacement == 3:
                posXA = posX+1
                posYA = posY-1
            elif deplacement == 4:
                posXA = posX+1
            elif deplacement == 5:
                posXA = posX+1
                posYA = posY+1
            elif deplacement == 6:
                posYA = posY+1
            elif deplacement == 7:
                posXA = posX-1
                posYA = posY+1
            elif deplacement == 8:
                posXA = posX-1
            else:
                print("Deplacement entre (1 et 8 uniquement)")
                continue
            if 0 <= posXA < 5 and 0 <= posYA < 5 and self.model.plateau[posXA][posYA] == 0:
                self.model.plateau[posXA][posYA] = self.tour
                break

    def affiche_gagnant(self):
        self.model.gagnant = True
        print("Le joueur " + str(self.tour) + " à gagné \n")

    def ia_vs_ia(self):
        # Pose un premier pion aléatoirement
        x = randint(0, 4)
        y = randint(0, 4)
        self.model.pose_pion(x, y)
        self.affiche_plateau()

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

            # Rafraichit  le plateau de jeu
            self.affiche_plateau()
            sleep(1)


# Lancer le combat d'ia
model = Model(1, 1)
model.pMax_ias[1] = int(sys.argv[1])  # pMax j1
model.eval_ias[1] = int(sys.argv[2])  # eval j1
model.pMax_ias[2] = int(sys.argv[3])  # pMax j2
model.eval_ias[2] = int(sys.argv[4])  # eval j2

game = VueConsole(model)
game.ia_vs_ia()
