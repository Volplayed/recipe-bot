#filters class
class Filters_container():
    def __init__(self, ingredients: list, time: int, level: str):
        #variables to be used
        self.ingredients = ingredients
        self.time = time
        self.level = level


    #sets everything to default values
    def reset(self):
        self.ingredients = []
        self.time = 0
        self.level = "Any"

    #makes a beautiful current filter string
    def get_string(self):
        #ingredients string making
        ingredients = ''

        if len(self.ingredients) > 0:
            #get each ingredient and put into string
            for ingredient in self.ingredients:
                if ingredients == '': #is empty
                    ingredients += ingredient
                else:
                    ingredients += f', {ingredient}'
        else: #if no ingredients are set
            ingredients = 'Any'
        
        #time string making
        time = ''

        if self.time != 0: #if filter is set
            time = f"{self.time}"
        else:
            time = 'Any'
        
        #level string
        level = self.level

        #final string
        text = f"Currently applied filters:\nIngredients: {ingredients}\nTime: {time}\nComplexity: {level}"

        return text
    
    #returns dict with data
    def get_dict(self):
        data = {'ingredients' : self.ingredients, 'time' : self.time, 'level' : self.level}

        return data

    #set ingredients
    def set_ingredients(self, text : str):
        try:
            #clear current ingredients
            self.ingredients = []

            #split input
            ingredients = text.split(',')
            
            #check if Any word is in list and clear filter
            if "Any" in ingredients:
                self.ingredients = []
            
            #else add each ingredient to the list
            else:
                for ingredient in ingredients:
                    if (ingredient.strip()) != '': #is not empty string
                        self.ingredients.append(ingredient.strip())
        except:
            pass

    #set time
    def set_time(self, text : str):
        try:
            #clear current time
            self.time = 0

            #check if text is Any
            if text == "Any":
                self.time = 0
            
            #else put integer into time
            else:
                self.time = int(text.strip())
        except:
            pass
    
    #set level
    def set_level(self, text : str):
        try:
            #clear current level
            self.level = 'Any'

            #put input data to level
            self.level = text.strip()
        except:
            pass