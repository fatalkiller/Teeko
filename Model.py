# -*- coding: utf-8 -*-


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
    - IAenCours : boolean, vrai si l'IA est en cours de calcul
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
        self.IAenCours = False

    def changeTour(self):
        self.verifGagnant()
        if self.IAenCours or not self.gagnant:
            if self.tour == 1:
                self.tour = 2
            else:
                self.tour = 1

    def posePion(self, x, y):
        if self.plateau[x][y] == 0:
            self.plateau[x][y] = self.tour
            self.changeTour()
            self.pose -= 1
            return True
        return False

    def mouvementPossible(self, x, y):
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

    def addMouvementPossible(self, x, y):
        if self.plateau[x][y] == self.tour:
            self.supprimeDeplacement()
            self.pion = [x, y]
            deplacements = self.mouvementPossible(x, y)
            for d in deplacements:
                self.plateau[d[0]][d[1]] = 3
            return True
        return False

    def deplacePion(self, x, y):
        if self.plateau[x][y] == 3 or self.IAenCours:
            self.plateau[x][y] = self.tour
            self.plateau[self.pion[0]][self.pion[1]] = 0
            self.supprimeDeplacement()
            self.pion = [-1, -1]
            self.IAenCours = False
            self.changeTour()
            return True
        return False

    def verifGagnant(self):
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

    def getCaseValue(self, x, y):
        return self.plateau[x][y]

    def action(self, x, y):
        if self.pose:
            return self.posePion(x, y)
        elif self.addMouvementPossible(x, y):
            return True
        elif self.pion != [-1, -1]:
            return self.deplacePion(x, y)
        return False

    def supprimeDeplacement(self):
        for i in range(5):
            for j in range(5):
                if self.plateau[i][j] == 3:
                    self.plateau[i][j] = 0

    def getTour(self):
        return self.tour

    def getGagnant(self):
        return self.gagnant
