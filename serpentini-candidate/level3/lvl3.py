

# import libraries
import json

# read in data
with open('./data/input.json') as f:
    jsonData = json.load(f)
#print(jsonData)

gain = {}
pay = {}
fiche_paye = {}
for user in jsonData["users"]:
    months = []
    gain[user["id"]] = {}
    pay[user["id"]] = {}
    fiche_paye[user["id"]] = {}

    for deal in jsonData["deals"]: # research all months where the user has a deal
        date = '-'.join(deal["close_date"].split("-")[0:2])
        if deal["user"] == user["id"]:
            if date not in months:
                months.append(date)
                gain[user["id"]][date] = 0.
            pay[user["id"]][deal["id"]] = 0.
    cible = user["objective"]
    demi_cible = cible*0.5
    for deal in jsonData["deals"]:
        if deal["user"] == user["id"]:
            for month in months:
                date = '-'.join(deal["close_date"].split("-")[0:2])
                if date == month:
                    gain_old = gain[user["id"]][date]
                    gain[user["id"]][date] += deal["amount"]
                    if gain[user["id"]][date] <= demi_cible:
                        pay[user["id"]][deal["id"]] = deal["amount"]*0.05
                    elif demi_cible < gain[user["id"]][date] <= cible:
                        if gain_old > demi_cible:
                            pay[user["id"]][deal["id"]] = deal["amount"]*0.1
                        else:
                            pay[user["id"]][deal["id"]] = (gain[user["id"]][date]-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
                    else:
                        if gain_old > cible:
                            pay[user["id"]][deal["id"]] = deal["amount"]*0.15
                        elif gain_old > demi_cible:
                            pay[user["id"]][deal["id"]] = (gain[user["id"]][date]-cible)*0.15 + (cible-gain_old)*0.1
                        else:
                            pay[user["id"]][deal["id"]] = (gain[user["id"]][date]-cible)*0.15 + (cible-demi_cible)*0.1 + (demi_cible-gain_old)*0.05
    print(pay)
    months = []
    print(months)
    for deal in jsonData["deals"]: # research all months where the user has a deal
        date = '-'.join(deal["payment_date"].split("-")[0:2])
        if date not in months and deal["user"] == user["id"]:
            months.append(date)
            fiche_paye[user["id"]][date] = 0.
    for deal in jsonData["deals"]:
        if deal["user"] == user["id"]:
            for month in months:
                date = '-'.join(deal["payment_date"].split("-")[0:2])
                if date == month:
                    fiche_paye[user["id"]][date] += pay[user["id"]][deal["id"]]
print(fiche_paye)



