"""
Le programme doit fournir une réponse en moins d'une seconde.
Nous n'avons plus besoin d'explorer toutes les combinaisons possibles, ce qui, à mon avis, devrait
accélérer l'algorithme.
"""

"""
Ideas :
Idea A : select best investment based on its benefice(euros)
Idea B : select best investment based on its benefice(euros)/cost ratio = benefice(%)
Idea C : select best investment based on benefit(%) * benefit(euros) = benefit(%)*benefit(%)*cost
>>>in fact: better results with benefit(percent) on Sienna data

Idea D : select best investment based on benefit(%) / cost
>>>DivisionZero error ; if (0.1 + cost) >>> not good results

Choice type of algorithm
>>>https://fr.wikipedia.org/wiki/Algorithme_de_tri#Comparaison_des_algorithmes

Mes criteres:
-Je sors tous les algos instables

4 equivalences + 3 cas qui se démarquent
Tri par insertion :     temporelle : entre n et n² ;    spatiale : 1 ;
Tri à bulles :          temporelle : entre n et n² ;    spatiale : 1 ;
Tri cockail :           temporelle : entre n et n² ;    spatiale : 1 ;
Tri pair-impair :       temporelle : entre n et n² ;    spatiale : 1 ;
>>>interessants mais je pense que n² sera trop long

Tri arboresence :  :    temporelle : nlogn ;            spatiale : n ;  interessant
> Cependant, il est moins efficace car il nécessite de construire une structure de données complexe
alors que le tri rapide est un tri en place. Il n'est donc pas utilisé en pratique. 
 > écarté

Timsort :               temporelle : nlogn ;            spatiale : n ;  interessant
>Timsort est l'algorithme standard de tri utilisé par Python depuis la version 2.3. 
> L'algorithme procède en cherchant des monotonies, c'est-à-dire des parties de l'entrée déjà 
  correctement ordonnées, et peut de cette manière trier efficacement l'ensemble des données en
  procédant par fusions successives. Pour des entrées de petites tailles, il revient à effectuer
  un tri fusion. 

Tri fusion :            temporelle : entre n et nlogn ; spatiale : n ;  interessant
> + décrit et pseudo code disponible

Partons sur Timsort dans un premier temps.
Tri fusion choisi pour sa simplicité
"""

"""Le tri fusion se décrit naturellement sur des listes et c'est sur de telles structures qu'il est
à la fois le plus simple et le plus rapide.
Le principe de l'algorithme de tri fusion repose sur cette observation : le plus petit élément
de la liste à construire est soit le plus petit élément de la première liste, soit le plus petit
élément de la deuxième liste. Ainsi, on peut construire la liste élément par élément en retirant
tantôt le premier élément de la première liste, tantôt le premier élément de la deuxième liste
"""


import csv
from time import time


MAXIMUM_EXPENDITURE = 500

available_money = MAXIMUM_EXPENDITURE
actions_parameters = []  # will contain all actions and their relative information 


def getActionParametersFromACsvFile(csvFileName, headerActionName,
                                    headerActionCost, headerActionProfitPercent):
    """Opens a CSV file and gets parameters and prices of actions"""
    # CSV package ; method DictReader() : Cette méthode sait que la première ligne est un en-tête
    # et sauvegarde les autres lignes en tant que dictionnaires. Chaque clé est un nom de colonne
    # et la valeur est la valeur de la colonne

    with open(csvFileName) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for line in reader:
            # actions_parameters filling
            action_name = line[headerActionName]
            action_cost = float(line[headerActionCost])
            action_benefit_percent = float(line[headerActionProfitPercent])/100
            action_benefit_euros = action_cost * action_benefit_percent

            # DECISION ABOUT SORTING
            # 'action_benefit_percent' or 'action_benefit_percent * action_benefit_euros'
            sorting_criteria = action_benefit_percent  
            
            # Dictionnary solution
            #actions_parameters[line['Action-#']] = {'cost': action_cost, 
            #'benefit_euros' : action_benefit_euros, 
            #'benefit_euros_cost_ratio' : action_benefit_euros_cost_ratio}

            # List solution
            # Note : action_benefit_euros_benefit_percent first place
            # PLESE DO NOT CHANGE THE ORDER (see main() function hereunder)
            action_parameter = [sorting_criteria, action_benefit_euros, action_name, 
                                action_cost, action_benefit_percent] 
            actions_parameters.append(action_parameter)


def FusionPart_sortingAlgorithm(halfTablePartA, halfTablePartB, 
                                           indexOfParameterToSortBy):
    """'Fusion' part of the fusion algorithm"""
    # Source: https://www.delftstack.com/fr/howto/python/merge-sort-in-python/

    if not len(halfTablePartA) or not len(halfTablePartB):
        return halfTablePartA or halfTablePartB

    finalSortedTable = []
    i = 0
    j = 0
    
    # Tant que la finalSortedTable ne contient pas tous les éléments à trier 
    while (len(finalSortedTable) < len(halfTablePartA) + len(halfTablePartB)):

        # Le premier 'élément de liste qui n'a pas encore été trié (i et j incrémentés)' 
        # le plus petit/grand est gardé dans la table finale (le plus grand pour un tri 
        # décroissant)
        
        # halfTablePartA[i] < halfTablePartB[j]: est la ligne originelle, j'ajoute [...] pour trier 
        # selon un parametre ou un autre (prix, rendement, etc)
        if halfTablePartA[i][indexOfParameterToSortBy] > \
        halfTablePartB[j][indexOfParameterToSortBy]: 
            finalSortedTable.append(halfTablePartA[i])
            i+= 1
        else:
            finalSortedTable.append(halfTablePartB[j])
            j+= 1

        # Si toute la table A ou tout la table B a été triée , alors on fusionne la table finale
        # avec la table qui n'a pas été triée
        if i == len(halfTablePartA) or j == len(halfTablePartB):
            finalSortedTable.extend(halfTablePartA[i:] or halfTablePartB[j:])
            break
 
    return finalSortedTable


def sortingFusionPart_sortingAlgorithm(tableToSort, indexOfParameterToSortBy):
    """'sortingFusion' part of the fusion algorithm"""
    # Source : https://www.delftstack.com/fr/howto/python/merge-sort-in-python/

    tableToSortLenght = len(tableToSort)
    if tableToSortLenght <= 1: #2 in the source, but does not sort totally; I replace with 1
        return tableToSort
    else:
        halfTablePartA = sortingFusionPart_sortingAlgorithm(
            tableToSort[:int(tableToSortLenght/2)], indexOfParameterToSortBy
            )
        halfTablePartB = sortingFusionPart_sortingAlgorithm(
            tableToSort[int(tableToSortLenght/2):], indexOfParameterToSortBy
            )
        return FusionPart_sortingAlgorithm(halfTablePartA, halfTablePartB, 
                                                      indexOfParameterToSortBy)




def main(csvFileName, headerActionName, headerActionCost, headerActionProfitPercent):
    """Main function of the program"""

    start_total_time = time()
    global available_money
    bought_actions = []
    total_benefit=0
    total_cost=0


    print("PREDICTION ON FILE: ", csvFileName)
    
    getActionParametersFromACsvFile(csvFileName, headerActionName, headerActionCost,
                                    headerActionProfitPercent)

    sorted_actions = sortingFusionPart_sortingAlgorithm(actions_parameters, 
        indexOfParameterToSortBy = 0)  # Choice of sorting parameter = [0]
    #print(sorted_actions)

    for action in sorted_actions:
        if available_money >= action[3] and action[1] > 0:
            #buying
            bought_actions.append(action[2])
            available_money -= action[3]
            total_benefit += action[1]
            total_cost += action[3]

    print("Bought actions: ", bought_actions)
    print("Total_benefit: ", total_benefit) 
    print("Total_cost: ", total_cost) 

    end_total_time = time()
    spent_total_time = end_total_time - start_total_time
    print("Spent total time (includes opening file, etc):", spent_total_time)


# Execute main() function once only, please, if not, available money is not 500 at the start of
# the second execution
#main('part1_actions.csv', "Action-#","Cout_par_action_(en_euros)","Bénéfice_(après_2_ans)")
#main('Données_anterieures_de_Sienna/dataset1_Python+P7.csv', "name","price","profit")
main('Données_anterieures_de_Sienna/dataset2_Python+P7.csv', "name","price","profit")
