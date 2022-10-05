
# import libraries
import json

# read in data
with open('./data/input.json') as f:
    jsonData = json.load(f)

# parse data to get the total for each user
user = {}
for deal in jsonData["deals"]:
    if deal["user"] not in user: # initialize data in the user dict (only once to create the dict)
        user[deal["user"]] = {}
        user[deal["user"]]["total"] = deal["amount"]
        user[deal["user"]]["count"] = 1
    else: # update data in the user dict
        user[deal["user"]]["total"] += deal["amount"]
        user[deal["user"]]["count"] += 1
#print(user)

# calculate commissions for each user and write to output file
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
print(userDict)

# write out data
with open('./data/output.json', 'w') as f:
    json.dump(userDict, f)