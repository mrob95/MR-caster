from habanero import Crossref
import json

cr = Crossref()

x = cr.works(query = "the bible")


print(x["message"]["items"])

print()