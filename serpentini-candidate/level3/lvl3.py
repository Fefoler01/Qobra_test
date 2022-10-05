

# import libraries
import json

# read in data
with open('./data/input.json') as f:
    jsonData = json.load(f)

# initialize global data dicts
gain = {}
pay = {}
fiche_paye = {}

# research all months where the user has a closing deal
months = []
for deal in jsonData["deals"]:
    date = '-'.join(deal["close_date"].split("-")[0:2]) # select the close date of the deal in the format YYYY-MM
    if date not in months: # obtain all distinct months where the user has a deal
        months.append(date)
    if deal["user"] not in gain: # initialize data in the gain dict (only once to create the dict)
        gain[deal["user"]] = {}
    gain[deal["user"]][date] = 0.

# calculate the gain for each user and each month
# then calculate the pay in function of the gain
for deal in jsonData["deals"]:
    cible = jsonData["users"][deal["user"]-1]["objective"] # get the objective of the user (100%)
    demi_cible = cible*0.5 # get the demi-objective of the user (50%)
    date = '-'.join(deal["close_date"].split("-")[0:2])
    for month in months:
        if date == month:
            gain_old = gain[deal["user"]][date] # save the last gain of the user for the month
            gain[deal["user"]][date] += deal["amount"] # add the new gain of the user for the month
            if gain[deal["user"]][date] <= demi_cible: # if the gain is under the demi-objective
                pay[deal["id"]] = deal["amount"]*0.05
            elif demi_cible < gain[deal["user"]][date] <= cible: # if the gain is between the demi-objective and the objective
                if gain_old > demi_cible: # if the gain was already over the demi-objective
                    pay[deal["id"]] = deal["amount"]*0.1
                else: # if the gain was under the demi-objective
                    pay[deal["id"]] = (gain[deal["user"]][date]-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
            else: # if the gain is over the objective
                if gain_old > cible: # if the gain was already over the objective
                    pay[deal["id"]] = deal["amount"]*0.15
                elif gain_old > demi_cible: # if the gain was between the demi-objective and the objective
                    pay[deal["id"]] = (gain[deal["user"]][date]-cible)*0.15 + (cible-gain_old)*0.1
                else: # if the gain was under the demi-objective
                    pay[deal["id"]] = (gain[deal["user"]][date]-cible)*0.15 + (cible-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
print("pay :\n",pay)

# research all months where the user has a payment deal
months = []
for deal in jsonData["deals"]:
    date = '-'.join(deal["payment_date"].split("-")[0:2]) # select the payment date of the deal in the format YYYY-MM
    if date not in months:
        months.append(date)
    if deal["user"] not in fiche_paye: # initialize data in the fiche_paye dict (only once to create the dict)
        fiche_paye[deal["user"]] = {}
    fiche_paye[deal["user"]][date] = 0.

# calculate the fiche_paye for each user and each month
for deal in jsonData["deals"]:
    date = '-'.join(deal["payment_date"].split("-")[0:2]) 
    for month in months:
        if date == month:
            fiche_paye[deal["user"]][date] += pay[deal["id"]]
print("fiche_paye :\n",fiche_paye)

# regroup datas in the output dict
userDict = {"commissions": [fiche_paye], "deals": []}
for id in pay: # get the commission pay for each deal
    userDict["deals"].append({"id": id, "commission": str(round(pay[id],2))})

# write out data
with open('./data/output.json', 'w') as f:
    json.dump(userDict, f)
