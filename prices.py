import json
import datetime
import requests
import subprocess as sp
from bs4 import BeautifulSoup as BS

# Read price log:
plog = "prices_log.json"
L_changed = False
with open(plog) as f:
    L = json.load(f)

# Read card list:
with open("cards.json") as f:
    J = json.load(f)

# Get number of cards:
ncards = 0
for b in J:
    for e in J[b]["cards"]:
        ncards += 1

dsu = []
now = datetime.datetime.now()
thres = datetime.timedelta(hours=12)

# Oath of the Gatewatch cards (2015B):
j = 0
for block in J:
    for i,card in J[block]["cards"]:
        j += 1
        progress = "{0}/{1}".format(j, ncards)
        for i in range(len(progress)):
            print("\b", end="", flush=True)
        print(progress, end="", flush=True)

        # First, try to read from log, and avoid downloading if log
        # contains a recent (< 12H):
        price = None
        if card in L:
            # Check how long ago latest value logged:
            ds, p = L[card][-1]
            d = datetime.datetime.strptime(ds, "%Y-%m-%d.%H:%M")
            if now - d < thres:
                price = p

        if not price:
            # Get price from URL:
            cn = card.replace(" ", "+")
            bname = J[block]["name"].replace(" ","+")
            url = "https://es.magiccardmarket.eu/Products/Singles/{0}/{1}".format(bname, cn)
            html_string = requests.get(url).text
            soup = BS(html_string, "html.parser")

            price = soup.find("td", class_="outerRight col_Odd col_1 cell_2_1")
            price = price.string.split()[0].replace(",",".")
            price = float(price)

            # Update price in log:
            ds = datetime.datetime.strftime(now, "%Y-%m-%d.%H:%M")
            if not card in L:
                L[card] = []
            L[card].append([ds, price])
            L_changed = True

        # Save price for showing:
        dsu.append([price, card])

dsu.sort()
dsu.reverse()

print("")
for p,c in dsu:
    string = "{0:6.2f} eur {1}".format(p,c)
    print(string)

# Save log, if changed:
if L_changed:
    string = json.dumps(L, sort_keys=True, indent=4)
    with open(plog, "w") as f:
        f.write(string)
