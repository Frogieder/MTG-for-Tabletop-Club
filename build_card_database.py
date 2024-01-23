import json as json_magic
import os
import sqlite3
import download_oracle_cards

TABLE_NAME = "images"

if not os.path.exists("oracle-cards.json"):
    download_oracle_cards.main()

with open('oracle-cards.json', 'r') as f:
    jsondata = json_magic.loads(f.read())

sqlstatement = 'INSERT INTO images (name, image_uris, oracle_text) VALUES '
for json in jsondata:
    doable = True
    keylist = "("
    valuelist = "("
    firstPair = True
    for key, value in json.items():
        if key == "card_faces":
            doable = False
        if key not in ("name", "image_uris", "oracle_text"):
            continue
        if key == "image_uris":
            value = value["large"]
        if not firstPair:
            keylist += ", "
            valuelist += ", "
        firstPair = False
        keylist += key
        if type(value) is str:
            valuelist += "'" + value.replace("'", "''") + "'"
        else:
            valuelist += str(value)
    keylist += ")"
    valuelist += ")"
    if doable:
        sqlstatement += valuelist + ",\n"

sqlstatement = (sqlstatement + "('Placeholder', 'https://cards.scryfall.io/large/front/8/4/84bb6cda-2dd0-4ad7-82ef-8461588d83aa.jpg?1683555539', 'Placeholder');")

# with open("sql_statement.sql", "w") as file:
#    file.write(sqlstatement)

connection = sqlite3.connect("cards.sqlite")
connection.execute("DROP TABLE IF EXISTS images;")
connection.execute("CREATE TABLE images (name varchar(256), image_uris varchar(512), oracle_text varchar(1024))")

connection.execute(sqlstatement)
connection.commit()

connection.close()
