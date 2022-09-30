from multiprocessing.spawn import prepare
import sqlite3
import requests
from bs4 import BeautifulSoup

######################################################
#converting two strings with time, in format where hours are marked as hr and minutes as mins, into integer
def time_string_into_int(time_string_prep, time_string_cook):
    #splitting into 2 lists
    time1 = time_string_prep.split()
    time2 = time_string_cook.split()

    #counter for time
    time = 0

    #if hr (hours) are in the string make it 60 mins
    if 'hr' in time1:
        #hr index
        i = time1.index('hr')

        #number before hours
        num = int(time1[i - 1])

        #adding it to time
        time += num * 60
    
    #same but for another time
    if 'hr' in time2:
        #hr index
        i = time2.index('hr')

        #number before hours
        num = int(time2[i - 1])

        #adding it to time
        time += num * 60
    
    #if mins are in list (in order to avoid errors)
    if 'mins' in time1 and 'mins' in time2:
        #time lists mins index
        i1 = time1.index('mins')
        i2 = time2.index('mins')

        #numbers before mins
        num1 = int(time1[i1 - 1])
        num2 = int(time2[i2 - 1])

        #adding it to time
        time += num1 + num2
    
    return int(time)

#create list of ingredients in string
def create_ingredients(soup):
    #elements list
    elements = soup.find_all('li', attrs={"class" : "pb-xxs pt-xxs list-item list-item--separator"})

    ingredients = str()

    #going through all elements and adding its text to ingredits
    for element in elements:
        ingredients += f"{element.text}, "
    


    return ingredients

#create preperation time string
def create_preparation_time(soup):
    #cook and prep time elements
    elements = soup.find_all('time')

    #strings where elements[0] is prep time and elements[1] is cooking time
    try:
        text_prep = elements[0].text
    except:
        text_prep = "0 mins"    
    try:
        text_cook = elements[1].text
    except:
        text_cook = '0 mins'
        
    #integer of minutes to cook
    time = time_string_into_int(text_prep, text_cook)

    return time

#crete complicacity level string
def create_level(soup):
    #all elements of mini data list
    elements = soup.find_all('div', attrs={'class' : "icon-with-text__children"})

    #formated string. elements[1] because level is second element of the mini data list
    text = f"{elements[1].text}"
    
    #check if page has level by checking its length
    if len(text.split()) != 1:
        text = 'Unknown'.split()
    return ''.join(text)

#create preparation method string
def create_method(soup):
    #list element of method
    element = soup.find('ul', attrs={'class' : "grouped-list__list list"})

    #children elements of list with headers and text 
    step_elements = element.find_all('span')
    method_elements = element.find_all('p')
    
    text = str()

    #add each step and method text to the text string
    for i in range(len(step_elements)):
        text += f'{step_elements[i].text}\n'
        text += f'{method_elements[i].text}\n'
    
    return text

#create image link 
def create_image(soup):
    #parent element of image - image-container
    element = soup.find('div', attrs={'class' :'post-header__image-container'})

    #image element
    image = element.find('img', attrs={'class' : "image__img"})

    return image['src']
###########################################################################
#database creation or connection
db = sqlite3.connect("recipes.db")
cur = db.cursor()

#creation of a database table
try:
    cur.execute("CREATE TABLE recipe(name, ingredients, time, level, method, image, url)")
except:
    pass


#site to be scraped url
url=f'https://www.bbcgoodfood.com/recipes/collection/student-recipes'
response = requests.get(url)

#initilization of bs4
soup = BeautifulSoup(response.text, 'html.parser')

#list of a elements with link to the recipe
recipe_link_element_list = soup.find_all('a', attrs={"class":"link d-block"})

#list holding information in dicts that will be put in database
data = list()

for element in recipe_link_element_list:
    try:
        #make url to recipe from the element 
        link = element['href']
        recipe_url = f"https://www.bbcgoodfood.com{link}"
        
        #open recipe url
        response = requests.get(recipe_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #dish name
        name = soup.find('h1', attrs={"class" : "heading-1"}).text.strip()
        
        #dish ingredients
        ingredients = create_ingredients(soup)

        #dish preperation time
        time = create_preparation_time(soup)

        #dish complicacity level
        level = create_level(soup)
        
        #dish prepare method
        method = create_method(soup)
        
        #dish image link
        image = create_image(soup)
        
        #put everything into tuple and put onto data list
        recipe = (name, ingredients, time, level, method, image, recipe_url)
        
        data.append(recipe)
    
    except:
        pass
#put all gathered data into table
cur.executemany("INSERT INTO recipe VALUES(?, ?, ?, ?, ?, ?, ?)", data)

db.commit()

a = cur.execute("SELECT level FROM recipe")
print(a.fetchall())

