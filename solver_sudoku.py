from ortools.sat.python import cp_model
import time
import pandas as pd
import numpy as np
import sys

def sudoku():
    modele = cp_model.CpModel()
    if (int(sys.argv[1]) == 9):
        taille_cellule = 3 #POUR LE 9 * 9
    elif (int(sys.argv[1]) == 16):
        taille_cellule = 4   #POUR LE 16 * 16
    elif (int(sys.argv[1]) == 36):
        taille_cellule = 6   #POUR LE 36 * 36
    taille_ligne = taille_cellule**2
    ligne = list(range(0, taille_ligne))
    cellule = list(range(0, taille_cellule))

    # Remplissage grille de valeurs initiales
    grille = {}
    for i in ligne:
        for j in ligne:
            grille[(i, j)] = modele.NewIntVar(1, taille_ligne, 'grille %i %i' % (i, j))

    # Faire en sorte que les lignes soient différentes
    for i in ligne:
        modele.AddAllDifferent(grille[(i, j)] for j in ligne)

    # Faire en sorte que les colonnes soient différentes
    for j in ligne:
        modele.AddAllDifferent(grille[(i, j)] for i in ligne)

    # Faire en sorte que les cases dans les blocs soient différentes
    for i in cellule:
        for j in cellule:
            cellule_diff = []
            for ii in cellule:
                for jj in cellule:
                    cellule_diff.append(grille[(i * taille_cellule + ii, j * taille_cellule + jj)])
            modele.AddAllDifferent(cellule_diff)

    # Comparaison valeurs initiales
    for i in ligne:
        for j in ligne:
            if decoded_puzzle[i][j]:
                modele.Add(grille[(i,j)]==decoded_puzzle[i][j])

    # On fait tourner le solveur et on affiche le résultat
    solver = cp_model.CpSolver()
    status = solver.Solve(modele)
    if status == cp_model.OPTIMAL:
        ###### DECOMMENTER LA LIGNE JUSTE EN DESSOUS POUR AFFICHAGE DES DIFFERENTS RESULTATS ######
        for i in ligne:
            print([int(solver.Value(grille[(i, j)])) for j in ligne])
            #pass

if (int(sys.argv[1]) == 9):
    sudoku9 = pd.read_csv("sudoku.csv")
    start = time.time()
    print("Début de la résolution")
    for index in range(400):
        print("Grille numero" , index)
        print("\n")
        echantillon = sudoku9.loc[index] # LIGNE DU FICHIER QUE L'ON PREND
        def decode(sample: str) -> np.array:
            return np.array([np.array(list(sample[i:i+9])).astype(int) for i in range(0, len(sample), 9)])
        decoded_puzzle  = decode(echantillon['quizzes'])
        sudoku()
elif (int(sys.argv[1]) == 16):
    sudoku16 = pd.read_csv("sudoku_16_csv.csv")
    print("Début de la résolution")
    start = time.time()
    for index in range(len(sudoku16)):
        print("Grille numero" , index)
        print("\n")
        echantillon = sudoku16.loc[index] # LIGNE DU FICHIER QUE L'ON PREND
        echantillon = ','.join(echantillon)
        temp = []
        for i in range(len(echantillon)):
            value = int(echantillon[i], base=17)
            temp.append(value)
        def decode(temp: str) -> np.array:
            return np.array([np.array(list(temp[i:i+16])).astype(int) for i in range(0, len(temp), 16)])
        decoded_puzzle = decode(temp)
        sudoku()
elif (int(sys.argv[1]) == 36):
    sudoku36 = pd.read_csv("grilles36.csv")
    print("Début de la résolution")
    start = time.time()
    for index in range(4):
        print("Grille numero" , index)
        print("\n")
        echantillon = sudoku36.loc[index] # LIGNE DU FICHIER QUE L'ON PREND
        echantillon = ','.join(echantillon)
        temp = []
        for i in range(len(echantillon)):
            value = int(echantillon[i], base=36)
            temp.append(value)
        def decode(temp: str) -> np.array:
            return np.array([np.array(list(temp[i:i+36])).astype(int) for i in range(0, len(temp), 36)])
        decoded_puzzle = decode(temp)
        sudoku()

# print("Voici la grille initiale")
# print(decoded_puzzle)
# print("\n")

end = time.time()
elapsed = end - start

print(f'Temps d\'exécution : {elapsed:.3}s')
