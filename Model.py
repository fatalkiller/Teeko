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
        self.joueur1= j1
        self.joueur2= j2
        self.gagnant = False

    def changeTour(self):
        self.verifGagnant()
        if not self.gagnant:
            if self.tour == 1:
                self.tour = 2
                # Verifier si le Joueur 2 est une IA --> on effectue l'action de l'IA et on rechange de tour directement
            else:
                self.tour = 1
                # Verifier si le Joueur 1 est une IA --> on effectue l'action de l'IA et on rechange de tour directement

    def posePion(self,x,y):
        if self.plateau[x][y] == 0:
            self.plateau[x][y] = self.tour
            self.changeTour()
            self.pose -= 1
            return True
        return False

    def addMouvementPossible(self, x, y):
        p = self.plateau
        if p[x][y] == self.tour:
            self.supprimeDeplacement()
            self.pion = [x, y]
            if x > 0 and y > 0 and p[x - 1][y - 1] == 0:
                p[x - 1][y - 1] = 3
            if y > 0 and p[x][y - 1] == 0:
                p[x][y - 1] = 3
            if x < 4 and y > 0 and p[x + 1][y - 1] == 0:
                p[x + 1][y - 1] = 3
            if x < 4 and p[x + 1][y] == 0:
                p[x + 1][y] = 3
            if x < 4 and y < 4 and p[x + 1][y + 1] == 0:
                p[x + 1][y + 1] = 3
            if y < 4 and p[x][y + 1] == 0:
                p[x][y + 1] = 3
            if x > 0 and y < 4 and p[x - 1][y + 1] == 0:
                p[x - 1][y + 1] = 3
            if x > 0 and p[x - 1][y] == 0:
                p[x - 1][y] = 3
            return True
        return False

    def deplacePion(self, x, y):
        if self.plateau[x][y] == 3 :
            self.plateau[x][y] = self.tour
            self.plateau[self.pion[0]][self.pion[1]] = 0
            self.supprimeDeplacement()
            self.pion = [-1,-1]
            self.changeTour()
            return True
        return False

    def verifGagnant(self):
        p = self.plateau
        t = self.tour
        for i in range(5) :
            for j in range(5):
                if p[i][j]==t:
                    if i<2 and p[i+1][j]==t and p[i+2][j]==t and p[i+3][j]==t:
                        self.gagnant = True
                    elif i<2 and  j<2 and p[i+1][j+1]==t and p[i+2][j+2]==t and p[i+3][j+3]==t:
                        self.gagnant = True
                    elif j<2 and p[i][j+1]==t and p[i][j+2]==t and p[i][j+3]==t:
                        self.gagnant = True
                    elif j<2 and i>2 and p[i-1][j+1]==t and p[i-2][j+2]==t and p[i-3][j+3]==t:
                        self.gagnant = True
                    elif i<4 and j<4 and p[i+1][j]==t and p[i+1][j+1]==t and p[i][j+1]==t:
                        self.gagnant = True
                    return

    def getCaseValue(self, x, y):
        return self.plateau[x][y]

    def action(self, x, y):
        if self.pose :
            return self.posePion(x,y)
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