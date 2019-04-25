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
        if self.IAenCours or not self.verifGagnant():
            if self.tour == 1:
                self.tour = 2
                if self.joueur2 == 1 and not self.IAenCours:
                    self.IAenCours = True
                    self.minMaxPoseOuDeplace(0)
            else:
                self.tour = 1
                if self.joueur1 == 1 and not self.IAenCours:
                    self.IAenCours = True
                    self.minMaxPoseOuDeplace(0)
        else:
            self.gagnant = True

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
            self.pion = [-1,-1]
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
                        return True
                    elif i < 2 and  j < 2 and p[i+1][j+1] == p[i+2][j+2] == p[i+3][j+3] == t:
                        return True
                    elif j < 2 and p[i][j+1] == p[i][j+2] == p[i][j+3] == t:
                        return True
                    elif j < 2 and i > 2 and p[i-1][j+1] == p[i-2][j+2] == p[i-3][j+3] == t:
                        return True
                    elif i < 4 and j < 4 and p[i+1][j] == p[i+1][j+1] == p[i][j+1] == t:
                        return True
                    return False

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

    def minMaxPoseOuDeplace(self, profondeur):
        # change le tour (pas au lancement)
        if profondeur != 0:
            self.changeTour()
        # on vérifie si le coup est gagnant ou si on est arrivé à la profondeur voulu
        # --> on évalue le plateau à ce moment
        val = 0
        if self.gagnant:
            self.gagnant = False
            if profondeur%2 == 0:
                val = -100 + 5 * profondeur
            else:
                val = 100 - 5 * profondeur
        elif profondeur == 4:
            val = self.evaluation(profondeur)
        elif self.pose > 0:
            self.pose -= 1
            val = self.minMaxPose(profondeur)
            self.pose += 1
        else:
            val = self.minMaxDeplace(profondeur)
        if profondeur != 0:
            self.changeTour()
            self.gagnant = False
        return val

    def minMaxPose(self, profondeur):
        # initialisation
        p = self.plateau
        t = self.tour
        coup = []
        # on initialise a -1000 quand on cherche le coup max et 1000 quand on cherche le coup min
        val = -1000
        if profondeur%2 == 1:
            val = 1000
        # boucle permettant de savoir le meilleur coup
        for j in range(5) :
            for i in range(5):
                if p[i][j] == 0:
                    # on pose le pion
                    p[i][j] = t
                    vald = self.minMaxPoseOuDeplace(profondeur+1)
                    # on compare la valeur du déplacement avec celle stocké
                    # si la valeur est supérieur (max) ou inférieur (min)
                    # on sauvegarde la valeur du coup actuel ainsi que le coup et pion actuel
                    if (profondeur%2 == 0 and vald > val) or (profondeur%2 == 1 and vald < val):
                        val = vald
                        coup = [i, j]
                    # on enlève le pion
                    p[i][j] = 0
        # effectue le meilleur déplacement possible à la fin de l'execution complète (seulement à profondeur 0)
        if profondeur == 0:
            self.IAenCours = False
            self.posePion(coup[0], coup[1])
        return val

    def minMaxDeplace(self, profondeur):
        # initialisation
        p = self.plateau
        t = self.tour
        coup = []
        pion = []
        # on initialise a -1000 quand on cherche le coup max et 1000 quand on cherche le coup min
        val = -1000
        if profondeur%2 == 1:
            val = 1000
        # boucle permettant de savoir le meilleur coup
        for j in range(5) :
            for i in range(5):
                if p[i][j] == t:
                    deplacements = self.mouvementPossible(i, j)
                    for d in deplacements:
                        # on effectue le deplacement
                        p[i][j] = 0
                        p[d[0]][d[1]] = t
                        vald = self.minMaxPoseOuDeplace(profondeur+1)
                        # on compare la valeur du déplacement avec celle stocké
                        # si la valeur est supérieur (max) ou inférieur (min)
                        # on sauvegarde la valeur du coup actuel ainsi que le coup et pion actuel
                        if (profondeur%2 == 0 and vald > val) or (profondeur%2 == 1 and vald < val):
                            pion = [i, j]
                            val = vald
                            coup = d
                        # on annule le déplacement
                        p[i][j] = t
                        p[d[0]][d[1]] = 0
        # effectue le meilleur déplacement possible à la fin de l'execution complète (seulement à profondeur 0)
        if profondeur == 0:
            self.pion = pion
            self.deplacePion(coup[0], coup[1])
        return val

    def evaluation(self, profondeur):
        return 0