
def eval(model):
    return 0


def minPose(model, p, alpha, beta):
    # Teste si on doit poser ou déplacer un pion
    if model.pose == 0:
        return minDeplace(model, p, alpha, beta)

    # Vérif noeud terminal
    if model.gagnant:
        model.gagnant = False
        return 100 + p
    if p == 0:
        return eval(model)

    # Init v pour un min
    v = 1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Test si plateau[j][i] déjà pris
            # On pose le pion à l'endroit souhaité
            if model.pose_pion(j, i):
                val = maxPose(model, p - 1, alpha, beta)

                # p impair, alors on fait un min
                v = min(v, val)

                # On annule le coup effectué
                model.plateau[j][i] = 0
                model.change_tour()
                model.pose += 1

                # Arrêter la recherche dans cette branche
                # si valeur min actuelle est de toute façon minimale
                if v <= alpha:
                    return v

                # Diminue beta pour accélerer la recherche du max
                beta = min(beta, v)
    return v


def maxPose(model, p, alpha, beta):
    # Teste si on doit poser ou déplacer un pion
    if model.pose == 0:
        return maxDeplace(model, p, alpha, beta)

    # Vérif noeud terminal
    if model.gagnant:
        model.gagnant = False
        return -100 - p
    if p == 0:
        return eval(model)

    # Init v pour un max
    v = -1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Test si plateau[j][i] déjà pris
            # On pose le pion à l'endroit souhaité
            if model.pose_pion(j, i):
                val = minPose(model, p - 1, alpha, beta)

                # p pair, alors on fait un max
                v = max(v, val)

                # On annule le coup effectué
                model.plateau[j][i] = 0
                model.change_tour()
                model.pose += 1

                # Arrêter la recherche dans cette branche
                # si valeur max actuelle est de toute façon maximale
                if v >= beta:
                    return v

                # Diminue alpha pour accélerer la recherche du min
                alpha = max(alpha, v)
    return v


def minDeplace(model, p, alpha, beta):
    # Vérif noeud terminal
    if model.gagnant:
        model.gagnant = False
        return 100 + p
    if p == 0:
        return eval(model)

    # Init v pour un min
    v = 1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Teste si la position courante est occupée
            if model.plateau[j][i] == model.tour:
                moves = model.mouvementPossible(j, i)

                # On parcoure les mouvements possibles
                for m in moves:
                    # On déplace le pion
                    model.plateau[m[0]][m[1]] = model.tour
                    # On enlève le pion à l'emplacement précédent
                    model.plateau[j][i] = 0
                    model.change_tour()

                    val = maxDeplace(model, p - 1, alpha, beta)

                    # p impair, alors on fait un min
                    v = min(v, val)

                    # On annule le coup effectué
                    model.change_tour()
                    model.plateau[m[0]][m[1]] = 0
                    model.plateau[j][i] = model.tour

                    # Arrêter la recherche dans cette branche
                    # si valeur min actuelle est de toute façon minimale
                    if v <= alpha:
                        return v

                    # Diminue beta pour accélerer la recherche du max
                    beta = min(beta, v)
    return v


def maxDeplace(model, p, alpha, beta):
    # Vérif noeud terminal
    if model.gagnant:
        model.gagnant = False
        return -100 - p
    if p == 0:
        return eval(model)

    # Init v pour un max
    v = -1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Teste si la position courante est occupée
            if model.plateau[j][i] == model.tour:
                moves = model.mouvementPossible(j, i)

                # On parcoure les mouvements possibles
                for m in moves:
                    # On déplace le pion
                    model.plateau[m[0]][m[1]] = model.tour
                    # On enlève le pion à l'emplacement précédent
                    model.plateau[j][i] = 0
                    model.change_tour()

                    val = minDeplace(model, p - 1, alpha, beta)

                    # p pair, alors on fait un max
                    v = max(v, val)

                    # On annule le coup effectué
                    model.change_tour()
                    model.plateau[m[0]][m[1]] = 0
                    model.plateau[j][i] = model.tour

                    # Arrêter la recherche dans cette branche
                    # si valeur max actuelle est de toute façon maximale
                    if v >= beta:
                        return v

                    # Diminue alpha pour accélerer la recherche du min
                    alpha = max(alpha, v)
    return v


def minMaxPose(model, p, alpha, beta):
    # Init du coup retourné
    coup = []

    # Init v pour un max
    v = -1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Test si plateau[j][i] déjà pris
            # On pose le pion à l'endroit souhaité
            if model.pose_pion(j, i):
                val = minPose(model, p - 1, alpha, beta)

                # p pair, alors on fait un max
                if v < val:
                    v = val
                    coup = [j, i]

                # On annule le coup effectué
                model.plateau[j][i] = 0
                model.change_tour()
                model.pose += 1

                # Diminue alpha pour accélerer la recherche du min
                alpha = max(alpha, v)

    # On pose le pion au meilleur emplacement
    model.pose_pion(coup[0], coup[1])


def minMaxDeplace(model, p, alpha, beta):
    # Init du coup retourné
    coup = []

    # Init v pour un max
    v = -1000

    # Parcoure du tableau de jeu
    for i in range(5):
        for j in range(5):
            # Teste si la position courante est occupée
            if model.plateau[j][i] == model.tour:
                moves = model.mouvementPossible(j, i)

                # On parcoure les mouvements possibles
                for m in moves:
                    # On déplace le pion
                    model.plateau[m[0]][m[1]] = model.tour
                    # On enlève le pion à l'emplacement précédent
                    model.plateau[j][i] = 0
                    model.change_tour()

                    val = minDeplace(model, p - 1, alpha, beta)

                    # p pair, alors on fait un max
                    if v < val:
                        v = val
                        model.pion = [j, i]
                        coup = m

                    # On annule le coup effectué
                    model.change_tour()
                    model.plateau[m[0]][m[1]] = 0
                    model.plateau[j][i] = model.tour

                    # Diminue alpha pour accélerer la recherche du min
                    alpha = max(alpha, v)

    # On déplace le pion au meilleur emplacement
    model.deplace_pion(coup[0], coup[1])


def minMax(model, p):
    # Init alpha et beta a +/- "infini"
    alpha = -1000
    beta = 1000

    model.IAenCours = True
    if model.pose > 0:
        minMaxPose(model, p, alpha, beta)
    else:
        minMaxDeplace(model, p, alpha, beta)
    model.IAenCours = False
