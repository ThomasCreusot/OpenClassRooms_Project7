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
from time import time

MAXIMUM_EXPENDITURE = 500

available_money = MAXIMUM_EXPENDITURE

actions_parameters = {}  # will contain all actions and their relative information 
action_prices = [] # --> tuple? is more adapted ? ; will be used to limit purchasing

# all_investment_possibilities will contain all tables corresponding to a possibility of investment
all_investment_possibilities = []
first_investment_possibility = []  # will contain a possibility of investment
all_investment_possibilities.append(first_investment_possibility)

best_investment_actions = "unknown"
best_investment_cost = "unknown"
best_investment_benefit = "unknown"

all_investment_possibilities_which_respect_maximum_expenditure = []


def getActionParametersFromACsvFile(csvFileName):
    """Opens a CSV file and gets parameters and prices of actions"""
    # CSV package ; method DictReader() : Cette méthode sait que la première ligne est un en-tête et 
    # sauvegarde les autres lignes en tant que dictionnaires. Chaque clé est un nom de colonne et la 
    # valeur est la valeur de la colonne

    with open(csvFileName) as csv_file:
        reader = csv.DictReader(csv_file, delimiter=',')
        for line in reader:
            # actions_parameters filling
            action_cost = int(line['Cout_par_action_(en_euros)'])
            action_benefit_percent = float(line['Bénéfice_(après_2_ans)'])/100  # 7% is noted 7 in the table, as in client data
            action_benefit_euros = action_cost * action_benefit_percent
            actions_parameters[line['Action-#']] = [action_cost, action_benefit_euros]

            # actions_prices filling
            action_prices.append(int(line['Cout_par_action_(en_euros)']))

    # print(actions_parameters["Action-1"])


def getAListOfActionsKeys():
    """Returns a list of actions keys corresponding to actions_parameters dictionnary"""

    keys_list = []
    for key in actions_parameters:
        keys_list.append(key)
    return keys_list


def define_all_investment_possibilities(all_investment_possibilities, actions_parameters,
                                        keys_list):
    """Defines all investment possibilities (brute force algorithm)"""

    # For each action: 2 possibilities: 
    # 1.Do not buy it ; 2.Buy it if its price is <= available_money, 
    # Stop paramater for recursivity ? While available_money >= lowest action price 

    # Logique choisie: 
    # pour chaque action : je l'achette ou je ne l'achette pas : 
    # turn 1 : [""],[A]
    # turn 2 : ["", ""], ["", B],[A, ""],[A, B]

    # https://fr.acervolima.com/copie-de-tableaux-en-python/
    # I need to copy ('copie profonde') the tables 

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

    all_investment_possibilities_copy_for_a_loop = all_investment_possibilities.copy()
    # for computer memory : [action-3] is not interesting if we got [0,0,3,0,0,0,0,0,0,0,0,...]
    all_investment_possibilities.clear()

    for table_of_possibilities in all_investment_possibilities_copy_for_a_loop:
 
        if len(keys_list) == 0: 
            break

        elif len(keys_list) > 0:

            #Make a copy and do not buy the action
            table_of_possibilities_copy_without_buying = table_of_possibilities.copy()
            table_of_possibilities_copy_without_buying.append([0,0])
            all_investment_possibilities.append(table_of_possibilities_copy_without_buying)

            #Make a copy and buy the action from actions_parameters
            table_of_possibilities_copy_with_buying = table_of_possibilities.copy()
            table_of_possibilities_copy_with_buying.append(actions_parameters[keys_list[0]]) 
            all_investment_possibilities.append(table_of_possibilities_copy_with_buying)

    keys_list.pop(0)


def calculatingCostAndBenefitOfEachInvestment(all_investment_possibilities):
    for investment_possibility in all_investment_possibilities:
        # print(investment_possibility)
        # >>> #[0, 0, [0, 0], [30, 0.1], [50, 0.15], [70, 0.2], [0, 0], [0, 0], [22, 0.07], ...
        totalInvestmentCost = 0
        totalInvestmentBenefit = 0

        for action in investment_possibility:
            # Cost
            action_cost = action[0]
            totalInvestmentCost += action_cost
            # Benefit
            action_benefit = action[1]
            totalInvestmentBenefit += action_benefit

        # Keep only investment which respond to expenditure criteria
        if totalInvestmentCost <= MAXIMUM_EXPENDITURE:
            # print("totalInvestmentCost ",totalInvestmentCost)
            investment_possibility.append(totalInvestmentCost)
            investment_possibility.append(totalInvestmentBenefit)
            all_investment_possibilities_which_respect_maximum_expenditure.append(
                investment_possibility)


def comparing_each_investment_which_respect_maximum_expenditure(best_investment_actions, 
                                                                best_investment_cost, 
                                                                best_investment_benefit):
    # highest_investment_benefit initialisation
    highest_investment_benefit = 0

    for investment in all_investment_possibilities_which_respect_maximum_expenditure:
        if investment[-1] > highest_investment_benefit :
            highest_investment_benefit = investment[-1] 
            best_investment_actions = investment[:-2]
            best_investment_cost =  investment[-2]
            best_investment_benefit = investment[-1]
    return best_investment_actions, best_investment_cost, best_investment_benefit 


def display_best_investiment(best_investment_information):
    """Displays  the best investiment"""

    best_investment_actions = best_investment_information[0]
    best_investment_cost = best_investment_information[1]
    best_investment_benefit = best_investment_information[2]

    print("The BEST INVESTMENT")
    print("List of actions to buy           ", best_investment_actions)
    print("Total cost of the investment:    ", best_investment_cost)
    print("Total benefit of the investment: ", best_investment_benefit)


def main():
    start_total_time = time()
    getActionParametersFromACsvFile('part1_actions.csv')
    keys_list = getAListOfActionsKeys()

    start_define_all_investment_possibilities_time = time()
    for i in range(len(actions_parameters)):
        print(i)
        define_all_investment_possibilities(all_investment_possibilities, actions_parameters, 
                                            keys_list)
    #for investment in all_investment_possibilities:
    #    print(investment)
    end_define_all_investment_possibilities_time = time()

    start_calculatingCostAndBenefitOfEachInvestment_time = time()
    calculatingCostAndBenefitOfEachInvestment(all_investment_possibilities)
    end_calculatingCostAndBenefitOfEachInvestment_time = time()

    best_investment_information = comparing_each_investment_which_respect_maximum_expenditure(
        best_investment_actions, best_investment_cost, best_investment_benefit)
    display_best_investiment(best_investment_information)
    end_total_time = time()


    spent_total_time = end_total_time - start_total_time
    spent_define_all_investment_possibilities_time = end_define_all_investment_possibilities_time - start_define_all_investment_possibilities_time
    spent_calculatingCostAndBenefitOfEachInvestment_time = end_calculatingCostAndBenefitOfEachInvestment_time - start_calculatingCostAndBenefitOfEachInvestment_time

    print("spent_total_time (includes opening file, etc):", spent_total_time)
    print("spent_define_all_investment_possibilities_time:", spent_define_all_investment_possibilities_time)
    print("spent_calculatingCostAndBenefitOfEachInvestment_time:", spent_calculatingCostAndBenefitOfEachInvestment_time)


main()

