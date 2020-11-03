import pprint
import statistics
import sys
from gdascore.gdaAttack import gdaAttack
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
true_value = 181962 # supplementary knowledge

pp = pprint.PrettyPrinter(indent=4)
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
params['verbose'] = False
params["dp_budget"] = DP_EPSILON_BUDGET # add the parameter "budget" to parameters for the attack

pp.pprint(params)


#
# # -------------------  Exploration Phase  ------------------------
# # This attack doesn't require any exploratory queries
#
# # -------------------  Prior Knowledge Phase  --------------------
# # We use the prior knowledge for some values in the database.
# # For the given query, we know that the real value is = 181962
# # """Select count(*)
# #          from transactions
# #          where operation = 'VKLAD'
# #          """
true_value = 181962
# # -------------------  Attack Phase  -----------------------------
#

print("--------------------")
print("Running First Attack")
print("--------------------")
x = gdaAttack(params)

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

pp.pprint(replyCorrect)

# -------------------  Attack Evaluation Phase  ----------------------------



# see how close we get to the real value after averaging out the server replies
if 'answer' in replyCorrect:
    answers = replyCorrect['answer']
    flat_values = [item for sublist in answers for item in sublist]
    print(flat_values)
    average_value = statistics.mean(flat_values)
    difference = abs(average_value - true_value)

    # If the attack is successful, we get a value here that is close to the original one, so the difference is small
    print("The absolute difference between the averaged value and the true one is: ", difference)
    print("The privacy budget used through the queries was epsilon= ", budget_used)
else:
    print("Reply has an error")
    pp.pprint(replyCorrect)


x.cleanUp()



# -------------------  Attack with several queries on the same budget  --------------------
# Here, the attack is tested for the execution of several sequential queries.
# All of them consume from the same attack budget.

print("--------------------")
print("Running Second Attack")
print("--------------------")
y = gdaAttack(params)
query = {}
sql = """Select count(*)
         from transactions
         where operation = 'VKLAD'
         """
query['sql'] = sql
query['epsilon'] = 2

# We can ask several queries with the same budget
y.askAttack(query)
replyCorrect1 = y.getAttack()
y.askAttack(query)
replyCorrect2 = y.getAttack()

# collect answers
if 'answer' in replyCorrect1 and 'answer' in replyCorrect2:
    answers = [replyCorrect1['answer'], replyCorrect2['answer']]

    print("All answers are:")
    pp.pprint(replyCorrect1['answer'])
    pp.pprint(replyCorrect2['answer'])

    # get attack can say how much of the bugdet is still available
    remaining_eps = replyCorrect2['remaining_dp_budget']
    budget_used = DP_EPSILON_BUDGET - remaining_eps
    print("Total budget used:")
    pp.pprint(budget_used)

    # see how close we get to the real value after averaging out the server replies
    def flatten(l):
        return flatten(l[0]) + (flatten(l[1:]) if len(l) > 1 else []) if type(l) is list else [l]

    flat_values = flatten(answers)
    average_value = statistics.mean(flat_values)
    difference = abs(average_value - true_value)
    #
    # # If the attack is successful, we get a value here that is close to the original one, so the difference is small
    print("The absolute difference between the averaged value and the true one is: ", difference)
    print("The privacy budget used through the queries was epsilon= ", budget_used)
else:
    print("Reply has an error")
    pp.pprint(replyCorrect1)
    pp.pprint(replyCorrect2)


y.cleanUp()


# -------------------  Attack where budget is exceeded  --------------------
# Here, first query is okay, the second is not because it would exceed the budget

print("--------------------")
print("Running Third Attack")
print("--------------------")
z = gdaAttack(params)
query = {}
sql = """Select count(*)
         from transactions
         where operation = 'VKLAD'
         """
query['sql'] = sql
query['epsilon'] = 3

# We can ask several queries with the same budget
z.askAttack(query)
replyCorrect1 = z.getAttack()
z.askAttack(query)
replyCorrect2 = z.getAttack()

if 'answer' in replyCorrect1 and 'answer' in replyCorrect2:
    print("All answers are:")
    pp.pprint(replyCorrect1['answer'])

    # As the budget was exceeded, there is no answer field, but an error instead:
    pp.pprint(replyCorrect2)

    # get attack can say how much of the bugdet is still available
    remaining_eps = replyCorrect2['remaining_dp_budget']
    budget_used = DP_EPSILON_BUDGET - remaining_eps
    print("The privacy budget used through the queries was epsilon= ", budget_used)
else:
    print("Reply has an error")
    pp.pprint(replyCorrect1)
    pp.pprint(replyCorrect2)


z.cleanUp()
