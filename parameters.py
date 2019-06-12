# Elagage Alpha-Beta
elagage = True

# Tableau des poids de chaques case du plateau de jeu
# pour la méthode d'évaluation
tabScore = [
    [4, 6, 5, 6, 4],
    [6, 10, 10, 10, 6],
    [5, 10, 12, 10, 5],
    [6, 10, 10, 10, 6],
    [4, 6, 5, 6, 4]
]

# Tableau des niveaux d'IA
#[Niveau_IA, profondeur_max, evaluation_enable]
tabLevels = [
    [1, 1, 0],
    [2, 3, 0],
    [3, 3, 1],
    [4, 5, 0],
    [5, 5, 1],
]
# pMax = tabLevels[n][1]
# eval = tabLevels[n][2]
