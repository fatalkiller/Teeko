class Teeko:
    """ Classe principal du jeu
    - plateau : int[][]
        - 0 -> case vide
        - 1 -> pion j1
        - 2 -> pion j2
    - tour : int --> numéro du joueur
    - joueur1 : Joueur
    - joueur2 : Joueur
    - gagnant : boolean, vrai si un joueur a gagné
    """

    def __init__(self):
        self.plateau = []
        for i in range(0,5):
            self.plateau.append([])
            for j in range(0,5):
                self.plateau[i].append(0)
        self.tour = 1
        self.joueur1= 1
        self.joueur2= 2
        self.gagnant = False

    def affichePlateau(self):
        affichage = "-------------------------\n" \
            "| / | 0 | 1 | 2 | 3 | 4 |\n" \
            "-------------------------\n"
        for j in range(5):
            affichage += "| " + str(j) + " |"
            for i in range(5):
                sym = " "
                if self.plateau[i][j]==1:
                    sym = "O"
                if self.plateau[i][j]==2:
                    sym = "X"
                affichage+= " " + sym + " |"
            affichage+= "\n" \
                 "-------------------------\n"
        print(affichage)

    def changeTour(self):
        self.verifGagnant()
        if self.tour == 1 :
            self.tour = 2
        else :
            self.tour = 1
        self.affichePlateau()

    def tourDeJeu(self):
        self.affichePlateau()
        for i in range(0,8):
            self.posePion()
            self.changeTour()
            if self.gagnant :
                break

        while not self.gagnant:
            self.deplacePion()
            self.changeTour()


    def posePion(self):
        while True:
            posX = int(input('Veuillez rentrez la colonne du pion à posé (entre 0 et 4)  : \n'))
            posY = int(input('Veuillez rentrez la ligne du pion à posé (entre 0 et 4)  : \n'))
            if 0 <= posX < 5 and 0 <= posY < 5 and self.plateau[posX][posY] == 0:
                self.plateau[posX][posY]=self.tour
                break
            print('mauvaise position')



    def deplacePion(self):
        while True:
            posX = int(input('Veuillez rentrez la colonne du pion à déplacer (entre 0 et 4)  : \n'))
            posY = int(input('Veuillez rentrez la ligne du pion à déplacer (entre 0 et 4)  : \n'))
            if posX<0 or posX>4 or posY<0 or posY>4 :
                print("numéro de ligne est colonne entre 0 et 4 ! \n")
            elif self.plateau[posX][posY]==self.tour:
                    break
            else :
                print("Aucun pion de votre couleur à cette position ! \n")

        self.plateau[posX][posY]=0

        posXA = posX
        posYA = posY
        while True:
            deplacement = int(input('Veuillez rentrez le deplacement du pion (entre 1 et 8 dans le sens des aiguilles d une montre en partant du haut à gauche)  : \n'))
            if deplacement == 1 :
                posXA = posX-1
                posYA = posY-1
            elif deplacement == 2 :
                posYA = posY-1
            elif deplacement == 3 :
                posXA = posX+1
                posYA = posY-1
            elif deplacement == 4 :
                posXA = posX+1
            elif deplacement == 5 :
                posXA = posX+1
                posYA = posY+1
            elif deplacement == 6 :
                posYA = posY+1
            elif deplacement == 7 :
                posXA = posX-1
                posYA = posY+1
            elif deplacement == 8 :
                posXA = posX-1
            else :
                print("Deplacement entre (1 et 8 uniquement)")
                continue
            if 0 <= posXA < 5 and 0 <= posYA < 5 and self.plateau[posXA][posYA]==0:
                self.plateau[posXA][posYA] = self.tour
                break




    def verifGagnant(self):
        p = self.plateau
        t = self.tour
        for i in range(0,4) :
            for j in range(0,4):
                if p[i][j]==t:
                    if i<2 and p[i+1][j]==t and p[i+2][j]==t and p[i+3][j]==t:
                        self.afficheGagnant()
                    elif i<2 and  j<2 and p[i+1][j+1]==t and p[i+2][j+2]==t and p[i+3][j+3]:
                        self.afficheGagnant()
                    elif j<2 and p[i][j+1]==t and p[i][j+2]==t and p[i][j+3]==t:
                        self.afficheGagnant()
                    elif j<2 and i>2 and p[i-1][j+1]==t and p[i-2][j+2]==t and p[i-3][j+3]:
                        self.afficheGagnant()
                    elif i<4 and j<4 and p[i+1][j]==t and p[i+1][j+1]==t and p[i][j+1]==t:
                        self.afficheGagnant()
                    return

    def afficheGagnant(self):
        self.gagnant = True
        print ("Le joueur " + str(self.tour) + " à gagné \n")


partie = Teeko()
partie.tourDeJeu()