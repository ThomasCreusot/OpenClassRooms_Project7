"""
Le programme doit fournir une réponse en moins d'une seconde.
Nous n'avons plus besoin d'explorer toutes les combinaisons possibles, ce qui, à mon avis, devrait accélérer l'algorithme.
"""

"""
Two ideas : 
Idea A : select best investment based on its benefice
Idea B : select best investment based on its benefice/cost ratio

Choice type of algorithm 
>>>https://fr.wikipedia.org/wiki/Algorithme_de_tri#Comparaison_des_algorithmes

Mes criteres: 
-Je sors tous les algos instables


4 equivalences + 2 cas qui se démarquent
Tri par insertion :     temporelle : entre n et n² ;    spatiale : 1 ;      interessant mais je pense que n² sera trop long
Tri à bulles :          temporelle : entre n et n² ;    spatiale : 1 ;      interessant mais je pense que n² sera trop long
Tri cockail :           temporelle : entre n et n² ;    spatiale : 1 ;      interessant mais je pense que n² sera trop long
Tri pair-impair :       temporelle : entre n et n² ;    spatiale : 1 ;      interessant mais je pense que n² sera trop long

Tri arboresence :  :    temporelle : nlogn ;            spatiale : n ;  interessant
> Cependant, il est moins efficace car il nécessite de construire une structure de données complexe alors que le tri rapide est un tri en place. Il n'est donc pas utilisé en pratique. 
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
"""

import csv


MAXIMUM_EXPENDITURE = 500

available_money = MAXIMUM_EXPENDITURE

actions_parameters = []  # will contain all actions and their relative information 

def getActionParametersFromACsvFile(csvFileName):
    """Opens a CSV file and gets parameters and prices of actions"""
    # CSV package ; method DictReader() : Cette méthode sait que la première ligne est un en-tête et 
    # sauvegarde les autres lignes en tant que dictionnaires. Chaque clé est un nom de colonne et la 
    # valeur est la valeur de la colonne

    with open(csvFileName) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for line in reader:
            # actions_parameters filling
            action_name = line['Action-#']
            action_cost = int(line['Cout_par_action_(en_euros)'])
            action_benefit_percent = float(line['Bénéfice_(après_2_ans)'])
            action_benefit_euros = action_cost * action_benefit_percent
            action_benefit_euros_cost_ratio = action_benefit_euros / action_cost
            
            #Dictionnary
            #actions_parameters[line['Action-#']] = {'cost': action_cost, 'benefit_euros' : action_benefit_euros, 'benefit_euros_cost_ratio' : action_benefit_euros_cost_ratio}
            #List
            action_parameter = [action_benefit_euros_cost_ratio, action_benefit_euros, action_name, action_cost] #action_benefit_euros_cost_ratio first place
            actions_parameters.append(action_parameter)

    # print(actions_parameters["Action-1"])


def FusionPart_sortingAlgorithm_by_benefit(halfTablePartA, halfTablePartB, indexOfParameterToSortBy):
    # https://www.delftstack.com/fr/howto/python/merge-sort-in-python/

    if not len(halfTablePartA) or not len(halfTablePartB):
        return halfTablePartA or halfTablePartB

    finalSortedTable = []
    i = 0
    j = 0
    
    #tant que la finalSortedTable ne contient pas tous les éléments à trier 
    while (len(finalSortedTable) < len(halfTablePartA) + len(halfTablePartB)):

        #le premier 'élément de liste qui n'a pas encore été trié (i et j incrémentés)' le plus petit est gardé dans la table finale
        if halfTablePartA[i][indexOfParameterToSortBy] > halfTablePartB[j][indexOfParameterToSortBy]: #halfTablePartA[i] < halfTablePartB[j]: est la ligne originelle, j'ajoute [...] pour trier selon un parametre ou un autre (prix, rendement, etc)
            finalSortedTable.append(halfTablePartA[i])
            i+= 1
        else:
            finalSortedTable.append(halfTablePartB[j])
            j+= 1



        #si toute la table A ou tout la table B a été triée , alors on fusionne la table finale avec la table qui n'a pas été triée
        if i == len(halfTablePartA) or j == len(halfTablePartB):
            finalSortedTable.extend(halfTablePartA[i:] or halfTablePartB[j:])
            break
 
    return finalSortedTable



def sortingFusionPart_sortingAlgorithm_by_benefit(tableToSort, indexOfParameterToSortBy):
    # https://www.delftstack.com/fr/howto/python/merge-sort-in-python/

    tableToSortLenght = len(tableToSort)
    if tableToSortLenght <= 1: #2 in the source, but does not sort totally
        return tableToSort
    else:
        halfTablePartA = sortingFusionPart_sortingAlgorithm_by_benefit(tableToSort[:int(tableToSortLenght/2)], indexOfParameterToSortBy)
        halfTablePartB = sortingFusionPart_sortingAlgorithm_by_benefit(tableToSort[int(tableToSortLenght/2):], indexOfParameterToSortBy)
        return FusionPart_sortingAlgorithm_by_benefit(halfTablePartA, halfTablePartB, indexOfParameterToSortBy)




"""Le tri fusion se décrit naturellement sur des listes et c'est sur de telles structures qu'il est à la fois le plus simple et le plus rapide. """

"""Le principe de l'algorithme de tri fusion repose sur cette observation : le plus petit élément
 de la liste à construire est soit le plus petit élément de la première liste, soit le plus petit
  élément de la deuxième liste. Ainsi, on peut construire la liste élément par élément en
   retirant tantôt le premier élément de la première liste, tantôt le premier élément de
    la deuxième liste """




"""
def sortingAlgorithm_by_benefitCostRatio(actions_parameters):
    for action in actions_parameters:
        print(actions_parameters[action])
"""


def main():
    getActionParametersFromACsvFile('part1_actions.csv')
    sorted_actions = sortingFusionPart_sortingAlgorithm_by_benefit(actions_parameters, indexOfParameterToSortBy = 2) #ON CHOISIR PAR QUOi TRIER ICI
    print(sorted_actions)

    global MAXIMUM_EXPENDITURE

    bought_actions = []
    total_benefit=0
    for action in sorted_actions:
        if MAXIMUM_EXPENDITURE >= action[3]:
            
            #buying
            bought_actions.append(action[2])
            MAXIMUM_EXPENDITURE -= action[3]
            total_benefit += action[1]

    print("bought_actions", bought_actions)
    print("total_benefit", total_benefit) #REPRENDRE ICI : j'ai trié dans le mauvais ordre --> j'ai modifié à la ligne 86; vérifier que tout est ok t



main()

