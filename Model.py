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
        for i in range(5) :
            for j in range(5):
                if self.plateau[i][j] == 3:
                    self.plateau[i][j] = 0

    def getTour(self):
        return self.tour

    def getGagnant(self):
        return self.gagnant

    def eval(self):
        return 0

    def minPose(self, p):
        # Teste si on doit poser ou déplacer un pion
        if self.pose == 0:
            return self.minDeplace(p)

        # Vérif noeud terminal
        if self.gagnant:
            self.gagnant = False
            return 100 + p
        if p == 0:
            return self.eval()

        # Init v pour un min
        v = 1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Test si plateau[j][i] déjà pris
                # On pose le pion à l'endroit souhaité
                if self.posePion(j, i):
                    val = self.maxPose(p-1)

                    # p impair, alors on fait un min
                    v = min(v, val)

                    # On annule le coup effectué
                    self.plateau[j][i] = 0
                    self.changeTour()
                    self.pose += 1
        return v

    def maxPose(self, p):
        # Teste si on doit poser ou déplacer un pion
        if self.pose == 0:
            return self.maxDeplace(p)

        # Vérif noeud terminal
        if self.gagnant:
            self.gagnant = False
            return -100 - p
        if p == 0:
            return self.eval()

        # Init v pour un max
        v = -1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Test si plateau[j][i] déjà pris
                # On pose le pion à l'endroit souhaité
                if self.posePion(j, i):
                    val = self.minPose(p - 1)

                    # p pair, alors on fait un max
                    v = max(v, val)

                    # On annule le coup effectué
                    self.plateau[j][i] = 0
                    self.changeTour()
                    self.pose += 1
        return v

    def minDeplace(self, p):
        # Vérif noeud terminal
        if self.gagnant:
            self.gagnant = False
            return 100 + p
        if p == 0:
            return self.eval()

        # Init v pour un min
        v = 1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Teste si la position courante est occupée
                if self.plateau[j][i] == self.tour:
                    moves = self.mouvementPossible(j, i)

                    # On parcoure les mouvements possibles
                    for m in moves:
                        # On déplace le pion
                        self.plateau[m[0]][m[1]] = self.tour
                        # On enlève le pion à l'emplacement précédent
                        self.plateau[j][i] = 0
                        self.changeTour()

                        val = self.maxDeplace(p-1)

                        # p impair, alors on fait un min
                        v = min(v, val)

                        # On annule le coup effectué
                        self.changeTour()
                        self.plateau[m[0]][m[1]] = 0
                        self.plateau[j][i] = self.tour
        return v

    def maxDeplace(self, p):
        # Vérif noeud terminal
        if self.gagnant:
            self.gagnant = False
            return -100 - p
        if p == 0:
            return self.eval()

        # Init v pour un max
        v = -1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Teste si la position courante est occupée
                if self.plateau[j][i] == self.tour:
                    moves = self.mouvementPossible(j, i)

                    # On parcoure les mouvements possibles
                    for m in moves:
                        # On déplace le pion
                        self.plateau[m[0]][m[1]] = self.tour
                        # On enlève le pion à l'emplacement précédent
                        self.plateau[j][i] = 0
                        self.changeTour()

                        val = self.minDeplace(p-1)

                        # p pair, alors on fait un max
                        v = max(v, val)

                        # On annule le coup effectué
                        self.changeTour()
                        self.plateau[m[0]][m[1]] = 0
                        self.plateau[j][i] = self.tour
        return v

    def minMaxPose(self, p):
        # Init du coup retourné
        coup = []

        # Init v pour un max
        v = -1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Test si plateau[j][i] déjà pris
                # On pose le pion à l'endroit souhaité
                if self.posePion(j, i):
                    val = self.minPose(p-1)

                    # p pair, alors on fait un max
                    if v < val:
                        v = val
                        coup = [j, i]

                    # On annule le coup effectué
                    self.plateau[j][i] = 0
                    self.changeTour()
                    self.pose += 1

        # On pose le pion au meilleur emplacement
        self.posePion(coup[0], coup[1])

    def minMaxDeplace(self, p):
        # Init du coup retourné
        coup = []

        # Init v pour un max
        v = -1000

        # Parcoure du tableau de jeu
        for i in range(5):
            for j in range(5):
                # Teste si la position courante est occupée
                if self.plateau[j][i] == self.tour:
                    moves = self.mouvementPossible(j, i)

                    # On parcoure les mouvements possibles
                    for m in moves:
                        # On déplace le pion
                        self.plateau[m[0]][m[1]] = self.tour
                        # On enlève le pion à l'emplacement précédent
                        self.plateau[j][i] = 0
                        self.changeTour()

                        val = self.minDeplace(p - 1)

                        # p pair, alors on fait un max
                        if v < val:
                            v = val
                            self.pion = [j, i]
                            coup = m

                        # On annule le coup effectué
                        self.changeTour()
                        self.plateau[m[0]][m[1]] = 0
                        self.plateau[j][i] = self.tour

        # On déplace le pion au meilleur emplacement
        self.deplacePion(coup[0], coup[1])

    def minMax(self, p):
        self.IAenCours = True
        if self.pose > 0:
            self.minMaxPose(p)
        else:
            self.minMaxDeplace(p)
        self.IAenCours = False