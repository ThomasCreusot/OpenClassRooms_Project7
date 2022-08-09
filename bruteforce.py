"""Votre algorithme doit suggérer une liste des actions les plus rentables que nous devrions 
acheter pour maximiser le profit d'un client au bout de deux ans."""

"""Nous avons les contraintes suivantes :
-Chaque action ne peut être achetée qu'une seule fois.
-Nous ne pouvons pas acheter une fraction d'action.
-Nous pouvons dépenser au maximum 500 euros par client.

Parce que nous voulons être aussi transparents que possible pour nos clients, nous voulons que le 
programme essaie toutes les différentes combinaisons d'actions qui correspondent 
à nos contraintes, et choisisse le meilleur résultat.  
Le programme doit donc lire un fichier contenant des informations sur les actions, explorer toutes 
les combinaisons possibles et afficher le meilleur investissement.
"""

import csv
from glob import glob

MAXIMUM_EXPENDITURE = 500

available_money = MAXIMUM_EXPENDITURE

actions_parameters = {} #contiendra toutes les actions et les informations qui leur sont relatives
action_prices = [] # --> tuple? is more adapted ?


all_possibilities_of_actions_bought_list_format = [] # --> table adapted ?

# PSEUDO CODE
# OPEN A FILE
# CSV package ; method DictReader() : Cette méthode sait que la première ligne est un en-tête et 
# sauvegarde les autres lignes en tant que dictionnaires. 
# Chaque clé est un nom de colonne et la valeur est la valeur de la colonne
# import csv
# with open('part1_actions.csv') as csv_file:
#   reader = csv.DictReader(csv_file, delimiter=',')
#   for line in reader:
#      print(line['Action-#'])

with open('part1_actions.csv') as csv_file:
    reader = csv.DictReader(csv_file, delimiter=',')
    for line in reader:
        # actions_parameters filling
        actions_parameters[line['Action-#']] = [int(line['Cout_par_action_(en_euros)']), 
                                                float(line['Bénéfice_(après_2_ans)'])]
        # actions_prices filling
        action_prices.append(int(line['Cout_par_action_(en_euros)']))

#print(actions_parameters["Action-1"])

# PSEUDO CODE
# EXPLORE ALL POSSIBILITIES
# For each action : 2 possibilities : 1.I do not buy it ; 2.I buy it if I can (if its price is <= available_money), 
# before coding : which is the stop paramater for recursivity ? answer : while available_money >= lowest action price 


#Logique choisie: 
#pour chaque action : je l'achette ou je ne l'achette pas : 
# [""],[A]
# ["", ""], ["", B],[A, ""],[A, B]

#print(actions_parameters)
# >>>{'Action-1': [20, 0.05], 'Action-2': [30, 0.1], 'Action-3': [50, 0.15], 'Action-4': [70, 0.2]

#for action in actions_parameters:
#    print(action)
    # >>> Action-1
    # >>> Action-2
    # >>> Action-3
    # >>> Action-4


#https://fr.acervolima.com/copie-de-tableaux-en-python/
#Je vais copier mon tableau en entrée de fonction pour en obtenir deux différents; copie profonde



#pour chaque action de mon dictionnaire, je veux qu'il enregistre UNE action dans une table; UN ELEMENT CLE EST QUE la table est différente à chaque fois
#donc il doit en créer une. on verra comment se débrouiller apres
#il doit sortir l'action ajoutée de la liste des actions

all_investment_possibilities = []
first_investment_possibility = [""]
all_investment_possibilities.append(first_investment_possibility)

keys_list = []
for key in actions_parameters:
    #print(key)
    #print(dictionnary_of_actions[key])
    keys_list.append(key)

def define_buying_possibilities(all_investment_possibilities, actions_parameters):
    #print()
    #print("all_investment_possibilities", all_investment_possibilities)
    all_investment_possibilities_copy_for_a_loop = all_investment_possibilities.copy()
    all_investment_possibilities.clear() #for computer memory ! [action-3] is not interesting if I got [0,0,3,0,0,0,0,0,0,0,0,...]

    for table_of_possibilities in all_investment_possibilities_copy_for_a_loop:
 
        if len(keys_list) == 1: #Si je mets zéro il me dit que je suis hors index par la suite... oui, parceque je rappelle à nouveau la fonction une dernière fois !
            break

        elif len(keys_list) > 1:

            #Make a copy and do not buy the action
            table_of_possibilities_copy_without_buying = table_of_possibilities.copy()
            table_of_possibilities_copy_without_buying.append("0")
            all_investment_possibilities.append(table_of_possibilities_copy_without_buying)
            #print(table_of_possibilities_copy_without_buying)

            #Make a copy and buy the action from actions_parameters
            table_of_possibilities_copy_with_buying = table_of_possibilities.copy()
            table_of_possibilities_copy_with_buying.append(actions_parameters[keys_list[0]]) 

            all_investment_possibilities.append(table_of_possibilities_copy_with_buying)
            #print(table_of_possibilities_copy_with_buying)
    keys_list.pop(0)
      
         

for i in range(len(actions_parameters)-1):
    print(i)
    define_buying_possibilities(all_investment_possibilities, actions_parameters)


for investment in all_investment_possibilities:
    print(investment)

# Recursivity
#mafonction(param1, param2):
#   début
#        si condition faire
#            retourner calcul
#        sinon faire
#            mafonction(param1, param2)
#            retourner quelque-chose
#        fin condition faire
#    fin
#fin ma fonction




# Display the best investment
#To be done











