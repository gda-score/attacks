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
from myUtilities import checkMatch

# Anon: None
# Attack: Identify values by averaging out the noise
# Criteria: Averaging out the noise
# Database: transactions

# -------------------------- body ---------------------------

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

# -------------------  Attack Phase  -----------------------------

query = {}
sql = """Select count(*)
         from transactions
         where operation = 'VKLAD'
         """
query['sql'] = sql
query['count'] = 3  # how often to execute the query
query['budget'] = 6.0
query['epsilon'] = 3
x.askAttack(query)
replyCorrect = x.getAttack()
if v: pp.pprint(replyCorrect)

# -------------------  Claims Phase  ----------------------------

# see how close we get to the real value after averaging out the server replies

x.cleanUp()

# here, potentially more queries could be executed, e.g. on the accounts DB
