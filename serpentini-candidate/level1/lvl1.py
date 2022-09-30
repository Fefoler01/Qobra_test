# 

# import libraries
import json

# read in data
with open('./data/input.json') as f:
    jsonData = json.load(f)
#print(jsonData)

# parse data
user = {}
for deal in jsonData["deals"]:
    #print(deal)
    if deal["user"] not in user:
        user[deal["user"]] = {}
        user[deal["user"]]["total"] = deal["amount"]
        user[deal["user"]]["count"] = 1
    else:
        user[deal["user"]]["total"] += deal["amount"]
        user[deal["user"]]["count"] += 1
#print(user)

# transform data
userDict = {"commissions": []}
for id in user:
    bonus=0
    if user[id]["total"]>=2000: # we give a bonus if the total is over 2000
        bonus=500

    if user[id]["count"]==0: # we give a compensation in function of the number of deals
        userDict["commissions"].append({"user_id": id, "commission": "0.00"})
    elif user[id]["count"]>=3:
        userDict["commissions"].append({"user_id": id, "commission": str(round(user[id]["total"]*0.2,2)+bonus)})
    else:
        userDict["commissions"].append({"user_id": id, "commission": str(round(user[id]["total"]*0.1,2)+bonus)})
#print(userDict)

# write out data
with open('./data/output.json', 'w') as f:
    json.dump(userDict, f)