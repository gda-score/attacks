import pprint

# import attack from local code in order to test
import sys
# currently need this to execute the local version of the project.
# when updated attack class is deployed, this line is obsolete
sys.path.insert(1, 'C:/Users/fra82576/PycharmProjects/gda-score/code/gdascore')

try:
    from .gdaAttack import gdaAttack
except ImportError:
    from gdaAttack import gdaAttack

# from .gdaAttack import gdaAttack
from gdascore.gdaScore import gdaScores
from gdascore.gdaTools import setupGdaAttackParameters


# Anon: None
# Attack: Identify values by averaging out the noise
# Criteria: Averaging out the noise
# Database: transactions

# -------------------------- body ---------------------------

# this sets the global attack budget for the specific attack we want to run
# this is epsilon, the DP privacy budget
DP_EPSILON_BUDGET = 5.0

pp = pprint.PrettyPrinter(indent=4)

verbose = 0
v = verbose
doCache = True

config = {
    "configVersion": "compact1",
    "basic": {
        "attackType": "Test",
        "criteria": "singlingOut"
    },
    'anonTypes': [['uber_anon']],
    'tables': [['banking', 'accounts']]
}

paramsList = setupGdaAttackParameters(config)
params = paramsList[0]
pp.pprint(params)

# add the parameter "budget" to parameters for the attack
params["dp_budget"] = DP_EPSILON_BUDGET


x = gdaAttack(params)

# -------------------  Exploration Phase  ------------------------
# This attack doesn't require any exploratory queries

# -------------------  Prior Knowledge Phase  --------------------
# We use the prior knowledge for some values in the database.
# For the given query, we know that the real value is = 181962
# """Select count(*)
#          from transactions
#          where operation = 'VKLAD'
#          """
true_value = 181962
# -------------------  Attack Phase  -----------------------------

query = {}
sql = """Select count(*)
         from transactions
         where operation = 'VKLAD'
         """
query['sql'] = sql
query['epsilon'] = 1
x.askAttack(query)
replyCorrect = x.getAttack()

# get attack can say how much of the bugdet is still available
remaining_eps = replyCorrect['remaining_dp_budget']

# initial bugdet - what is still available = budget used
budget_used = DP_EPSILON_BUDGET - remaining_eps

if v: pp.pprint(replyCorrect)

# -------------------  Claims Phase  ----------------------------

import statistics

# see how close we get to the real value after averaging out the server replies
answers = replyCorrect['answer']
flat_values = [item for sublist in answers for item in sublist]
average_value = statistics.mean(flat_values)
difference = abs(average_value - true_value)

# If the attack is successful, we get a value here that is close to the original one, so the difference is small
print("The absolute difference between the averaged value and the true one is: ", difference)
print("The privacy budget used through the queries was epsilon= ", budget_used)


x.cleanUp()



# -------------------  Attack with several queries on the same budget  --------------------


# -------------------  Prior Knowledge Phase  --------------------
# We use the prior knowledge for some values in the database.
# For the given query, we know that the real value is = 181962
# """Select count(*)
#          from transactions
#          where operation = 'VKLAD'
#          """


# true_value = 181962
# # # -------------------  Attack Phase  -----------------------------
# #
#
# y = gdaAttack(params)
# query = {}
# sql = """Select count(*)
#          from transactions
#          where operation = 'VKLAD'
#          """
# query['sql'] = sql
# query['epsilon'] = 1
#
# # We can ask several queries with the same budget
# y.askAttack(query)
# replyCorrect1 = y.getAttack()
# #y.askAttack(query)
# #y.askAttack(query)
# y.askAttack(query)
# replyCorrect2 = y.getAttack()
# pp.pprint(replyCorrect)
#
# # get attack can say how much of the bugdet is still available
# remaining_eps = replyCorrect['remaining_dp_budget']
#
# # initial bugdet - what is still available = budget used
# budget_used = DP_EPSILON_BUDGET - remaining_eps
#
# if v: pp.pprint(replyCorrect)
#
# # -------------------  Claims Phase  ----------------------------
#
# import statistics
#
# # see how close we get to the real value after averaging out the server replies
# answers = replyCorrect['answer']
# flat_values = [item for sublist in answers for item in sublist]
# average_value = statistics.mean(flat_values)
# difference = abs(average_value - true_value)
#
# # If the attack is successful, we get a value here that is close to the original one, so the difference is small
# print("The absolute difference between the averaged value and the true one is: ", difference)
# print("The privacy budget used through the queries was epsilon= ", budget_used)
#
#
# y.cleanUp()
