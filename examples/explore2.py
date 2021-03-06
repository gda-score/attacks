import pprint
from gdascore.gdaAttack import gdaAttack
from gdascore.gdaTools import setupGdaAttackParameters

# This script examines the schema of a raw database and
# stores the schema (table names, column names and types) in a data
# structure. It also makes a few simple queries. This is for testing
# where params don't include anonDb or criteria.

pp = pprint.PrettyPrinter(indent=4)

config = {
    'anonTypes': [ ['diffix','latest'] ],
    'tables': [ ['banking','accounts'] ]
}

paramsList = setupGdaAttackParameters(config)
params = paramsList[0]
pp.pprint(params)
x = gdaAttack(params)

# Start by exploring tables and columns
# First a list of tables from the raw (postgres) database

print("Tables and columns in both databases using class methods")
tables = x.getTableNames(dbType='rawDb')
pp.pprint(tables)
for table in tables:
    print(f"    {table}")
    cols = x.getColNamesAndTypes(dbType='rawDb', tableName=table)
    pp.pprint(cols)

sql = """SELECT tablename
         FROM pg_catalog.pg_tables
         WHERE schemaname != 'pg_catalog' AND
               schemaname != 'information_schema';"""
query = dict(db="raw", sql=sql)
x.askExplore(query)
rawTables = x.getExplore()
if not rawTables:
    x.cleanUp(exitMsg="Failed to get raw tables")
if 'error' in rawTables:
    x.cleanUp(exitMsg="Failed to get raw tables")
print("Tables in raw DB:")
for row in rawTables['answer']:
    print(f"   {row[0]}")

# Let's build data structures of tables and columns
rawInfo = {}
for tab in rawTables['answer']:
    tableName = tab[0]
    rawInfo[tableName] = {}
    sql = str(f"""select column_name, data_type 
                  from information_schema.columns where
                  table_name='{tableName}'""")
    query = dict(db="raw", sql=sql)
    x.askExplore(query)
    reply = x.getExplore()
    for row in reply['answer']:
        colName = row[0]
        colType = row[1]
        rawInfo[tableName][colName] = colType
pp.pprint(rawInfo)

query = dict(db="raw", sql="select count(*) from accounts")
for i in range(5):
    query['myTag'] = i
    x.askExplore(query)
while True:
    answer = x.getExplore()
    print(answer)
    tag = answer['query']['myTag']
    print(f"myTag is {tag}")
    if answer['stillToCome'] == 0:
        break

publicList = x.getPublicColValues("cli_district_id")
for entry in publicList:
    print(f"Value {entry[0]} has count {entry[1]}")
x.cleanUp()
