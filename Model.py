# -*- coding: utf-8 -*-
import parameters


class Model:
    """ Classe principal du jeu
    - plateau : int[][]
        - 0 -> case vide
        - 1 -> pion j1
        - 2 -> pion j2
    - pose : int -> nombre de pions a posé encore
    - tour : int --> numéro du joueur
    - pion : int[2] contient les coordonnées du dernier pion
    - joueur1 : Joueur // pour le moment 0 -> joueur et 1 -> IA
    - joueur2 : Joueur
    - gagnant : boolean, vrai si un joueur a gagné
    - ia_en_cours : int -> 0 si pas d'ia en cours, 1 si ia1 (joueur1), 2 si ia2 (joueur2)
    """

    TYPE_JOUEUR = 0     # Joueur humain
    TYPE_IA = 1         # Joueur IA

    def __init__(self, j1, j2):
        self.plateau = []
        for i in range(5):
            self.plateau.append([])
            for j in range(5):
                self.plateau[i].append(0)
        self.pose = 8
        self.tour = 1
        self.pion = [-1, -1]
        self.joueur1 = j1
        self.joueur2 = j2
        self.gagnant = False
        self.ia_en_cours = 0

    def change_tour(self):
        self.verif_gagnant()
        if self.ia_en_cours != 0 or not self.gagnant:
            if self.tour == 1:
                self.tour = 2
            else:
                self.tour = 1

    def pose_pion(self, x, y):
        if self.plateau[x][y] == 0:
            self.plateau[x][y] = self.tour
            self.change_tour()
            self.pose -= 1
            return True
        return False

    def mouvement_possible(self, x, y):
        p = self.plateau
        deplacements = []
        if x > 0 and y > 0 and p[x - 1][y - 1] == 0:
            deplacements.append([x-1, y-1])
        if y > 0 and p[x][y - 1] == 0:
            deplacements.append([x, y-1])
        if x < 4 and y > 0 and p[x + 1][y - 1] == 0:
            deplacements.append([x+1, y-1])
        if x < 4 and p[x + 1][y] == 0:
            deplacements.append([x+1, y])
        if x < 4 and y < 4 and p[x + 1][y + 1] == 0:
            deplacements.append([x+1, y+1])
        if y < 4 and p[x][y + 1] == 0:
            deplacements.append([x, y+1])
        if x > 0 and y < 4 and p[x - 1][y + 1] == 0:
            deplacements.append([x-1, y+1])
        if x > 0 and p[x - 1][y] == 0:
            deplacements.append([x-1, y])
        return deplacements

    def add_mouvement_possible(self, x, y):
        if self.plateau[x][y] == self.tour:
            self.supprime_deplacement()
            self.pion = [x, y]
            deplacements = self.mouvement_possible(x, y)
            for d in deplacements:
                self.plateau[d[0]][d[1]] = 3
            return True
        return False

    def deplace_pion(self, x, y):
        if self.plateau[x][y] == 3 or self.ia_en_cours != 0:
            self.plateau[x][y] = self.tour
            self.plateau[self.pion[0]][self.pion[1]] = 0
            self.supprime_deplacement()
            self.pion = [-1, -1]
            self.ia_en_cours = 0
            self.change_tour()
            return True
        return False

    def verif_gagnant(self):
        p = self.plateau
        t = self.tour
        for j in range(5):
            for i in range(5):
                if p[i][j] == t:
                    if i < 2 and p[i+1][j] == p[i+2][j] == p[i+3][j] == t:
                        self.gagnant = True
                    elif i < 2 and j < 2 and p[i+1][j+1] == p[i+2][j+2] == p[i+3][j+3] == t:
                        self.gagnant = True
                    elif j < 2 and p[i][j+1] == p[i][j+2] == p[i][j+3] == t:
                        self.gagnant = True
                    elif j < 2 < i and p[i - 1][j + 1] == p[i - 2][j + 2] == p[i - 3][j + 3] == t:
                        self.gagnant = True
                    elif i < 4 and j < 4 and p[i+1][j] == p[i+1][j+1] == p[i][j+1] == t:
                        self.gagnant = True
                    return

    def get_case_value(self, x, y):
        return self.plateau[x][y]

    def action(self, x, y):
        if self.pose:
            return self.pose_pion(x, y)
        elif self.add_mouvement_possible(x, y):
            return True
        elif self.pion != [-1, -1]:
            return self.deplace_pion(x, y)
        return False

    def supprime_deplacement(self):
        for i in range(5):
            for j in range(5):
                if self.plateau[i][j] == 3:
                    self.plateau[i][j] = 0

    def get_tour(self):
        return self.tour

    def get_gagnant(self):
        return self.gagnant

    def evaluation(self):
        score = 0
        for i in range(5):
            for j in range(5):
                if self.plateau[i][j] != 0:
                    if self.plateau[i][j] == self.ia_en_cours:
                        score += parameters.tabScore[i][j]
                    else:
                        score -= parameters.tabScore[i][j]
        return score
