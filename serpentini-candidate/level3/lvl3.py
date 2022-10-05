

# import libraries
import json

# read in data
with open('./data/input.json') as f:
    jsonData = json.load(f)
#print(jsonData)

gain = {}
pay = {}
fiche_paye = {}

months = []
for deal in jsonData["deals"]: # research all months where the user has a deal
    date = '-'.join(deal["close_date"].split("-")[0:2])
    if date not in months:
        months.append(date)
    if deal["user"] not in gain:
        gain[deal["user"]] = {}
    gain[deal["user"]][date] = 0.
#print(pay)
for deal in jsonData["deals"]:
    cible = jsonData["users"][deal["user"]-1]["objective"]
    demi_cible = cible*0.5
    for month in months:
        date = '-'.join(deal["close_date"].split("-")[0:2])
        if date == month:
            gain_old = gain[deal["user"]][date]
            gain[deal["user"]][date] += deal["amount"]
            if gain[deal["user"]][date] <= demi_cible:
                pay[deal["id"]] = deal["amount"]*0.05
            elif demi_cible < gain[deal["user"]][date] <= cible:
                if gain_old > demi_cible:
                    pay[deal["id"]] = deal["amount"]*0.1
                else:
                    pay[deal["id"]] = (gain[deal["user"]][date]-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
            else:
                if gain_old > cible:
                    pay[deal["id"]] = deal["amount"]*0.15
                elif gain_old > demi_cible:
                    pay[deal["id"]] = (gain[deal["user"]][date]-cible)*0.15 + (cible-gain_old)*0.1
                else:
                    pay[deal["id"]] = (gain[deal["user"]][date]-cible)*0.15 + (cible-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
print(pay)
months = []
for deal in jsonData["deals"]: # research all months where the user has a deal
    date = '-'.join(deal["payment_date"].split("-")[0:2])
    if date not in months:
        months.append(date)
    if deal["user"] not in fiche_paye:
        fiche_paye[deal["user"]] = {}
    fiche_paye[deal["user"]][date] = 0.
for deal in jsonData["deals"]:
    for month in months:
        date = '-'.join(deal["payment_date"].split("-")[0:2])
        if date == month:
            fiche_paye[deal["user"]][date] += pay[deal["id"]]
print(fiche_paye)

userDict = {"commissions": [fiche_paye], "deals": []}
for id in pay:
    userDict["deals"].append({"id": id, "commission": str(round(pay[id],2))})

# write out data
with open('./data/output.json', 'w') as f:
    json.dump(userDict, f)
