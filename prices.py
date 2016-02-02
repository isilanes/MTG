import json
import subprocess as sp
from bs4 import BeautifulSoup as BS

with open("cards.json") as f:
    J = json.load(f)

dsu = []
for card in J["ogw"]:
    cn = card.replace(" ", "+")
    url = "https://es.magiccardmarket.eu/Products/Singles/Oath+of+the+Gatewatch/{0}".format(cn)
    html = "tmp.html"
    s = sp.Popen("wget -q '{0}' -O {1}".format(url, html), shell=True)
    s.communicate()
    with open(html) as f:
        soup = BS(f, "html.parser")

    price = soup.find("td", class_="outerRight col_Odd col_1 cell_2_1")
    price = price.string.split()[0].replace(",",".")
    price = float(price)
    dsu.append([price, card])

dsu.sort()
dsu.reverse()

for p,c in dsu:
    string = "{0:6.2f} eur {1}".format(p,c)
    print(string)
