import sqlite3
from random import randint


#get random recipe
def get_random_recipe():
    #database creation or connection
    db = sqlite3.connect("recipes.db")
    cur = db.cursor()

    #get all recipe names
    names = cur.execute("SELECT name FROM recipe")
    names = names.fetchall()

    #get random name
    r = randint(0, len(names) - 1)
    name = names[r][0]

    #get all other elements from element with this name
    ingredients = cur.execute(f"SELECT ingredients FROM recipe WHERE name='{name}'")
    ingredients = ingredients.fetchone()[0]

    time = cur.execute(f"SELECT time FROM recipe WHERE name='{name}'")
    time = time.fetchone()[0]

    level = cur.execute(f"SELECT level FROM recipe WHERE name='{name}'")
    level = level.fetchone()[0]

    method = cur.execute(f"SELECT method FROM recipe WHERE name='{name}'")
    method = method.fetchone()[0]

    image = cur.execute(f"SELECT image FROM recipe WHERE name='{name}'")
    image = image.fetchone()[0]

    url = cur.execute(f"SELECT url FROM recipe WHERE name='{name}'")
    url = url.fetchone()[0]

    #gather all info into dict
    data = {
        'name' : name,
        'ingredients' : ingredients,
        'time' : time,
        'level' : level,
        'method' : method,
        'image' : image,
        'url' : url,
        }
    
    return data


