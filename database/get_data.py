import sqlite3
from random import randint
#get every otehr element with name of element
def get_other_elements(name, cur):
    #get all other elements from element with this name
    ingredients = cur.execute(f'''SELECT ingredients FROM recipe WHERE name="{name}"''')
    ingredients = ingredients.fetchone()[0]

    time = cur.execute(f'''SELECT time FROM recipe WHERE name="{name}"''')
    time = time.fetchone()[0]

    level = cur.execute(f'''SELECT level FROM recipe WHERE name="{name}"''')
    level = level.fetchone()[0]

    method = cur.execute(f'''SELECT method FROM recipe WHERE name="{name}"''')
    method = method.fetchone()[0]

    image = cur.execute(f'''SELECT image FROM recipe WHERE name="{name}"''')
    image = image.fetchone()[0]

    url = cur.execute(f'''SELECT url FROM recipe WHERE name="{name}"''')
    url = url.fetchone()[0]

    return ingredients, time, level, method, image, url

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
    ingredients, time, level, method, image, url = get_other_elements(name, cur)
    
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

#getting random recipe which fits the filters
def get_recipe_with_filters(filters : dict):
    #database creation or connection
    db = sqlite3.connect("recipes.db")
    cur = db.cursor()
 
    #get values from filters dict
    ingredients_filter = filters["ingredients"]
    time_filter = filters["time"]
    level_filter = filters["level"]

    #check what filters are applied
    if time_filter != 0 and type(time_filter) is int and level_filter == "Any": #if only time filter is applied
        #get names with this filter
        names = cur.execute(f"SELECT name FROM recipe WHERE time<={int(time_filter)}")
        names = names.fetchall()

    elif level_filter != "Any" and time_filter == 0: #if only level filter is applied
        #get names with this filter
        names = cur.execute(f"SELECT name FROM recipe WHERE level='{level_filter}'")
        names = names.fetchall()
    
    elif time_filter != 0 and type(time_filter) is int and level_filter != "Any": #if both level and time filters are applied
        #get names with these filters
        names = cur.execute(f"SELECT name FROM recipe WHERE level='{level_filter}' AND time<={int(time_filter)}")
        names = names.fetchall()
    
    #if only ingredients are set
    elif time_filter == 0 and level_filter == "Any" and ingredients_filter != []:
        names = cur.execute("SELECT name FROM recipe")
        names = names.fetchall()

    #if no filters are applied
    elif time_filter == 0 and level_filter == "Any" and ingredients_filter == []:
        #return random recipe
        data = get_random_recipe()
        return data
        
    #list with names which have appropriate ingredients
    appr_names = []

    #compare ingredients filter of every recipe from names
    for name in names:
        #get name from tuple
        name = name[0]
        #ingredients of recipe with name
        data_ingredients = cur.execute(f'''SELECT ingredients FROM recipe WHERE name="{name}"''')
        data_ingredients = data_ingredients.fetchone()

        #if has ingredients from filter save to list
        #temp int list
        temp = []
        for ingredient in ingredients_filter:
            
            #if ingredient in the data_ingredients save True
            if ingredient.lower() in data_ingredients[0].lower():
                temp.append(1)
            
            else:
                temp.append(0)
                break
            
        #if no False in temp add name to appr_names
        if 0 not in temp:
            appr_names.append(name)

    
    #get random name from appr_names
    r = randint(0, len(appr_names) - 1)
    name = appr_names[r]

    #get other elements
    ingredients, time, level, method, image, url = get_other_elements(name, cur)

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

