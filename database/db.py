from multiprocessing.spawn import prepare
import sqlite3
import requests
from bs4 import BeautifulSoup

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

    #formated string where elements[0] is prep time and elements[1] is cooking time
    text = f"Prep: {elements[0].text}, Cook: {elements[1].text}"

    return text

#crete complicacity level string
def create_level(soup):
    #all elements of mini data list
    elements = soup.find_all('div', attrs={'class' : "icon-with-text__children"})

    #formated string. elements[1] because level is second element of the mini data list
    text = f"{elements[1].text}"

    return text

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

#site to be scraped url
url='https://www.bbcgoodfood.com/recipes/collection/student-recipes?page=1'
response = requests.get(url)

#database creation
db = sqlite3.connect("recipes.db")
cur = db.cursor()

#creation of a database table
try:
    cur.execute("CREATE TABLE recipe(name, ingredients, time, level, method, image, url)")
except:
    pass

#initilization of bs4
soup = BeautifulSoup(response.text, 'html.parser')

#list of a elements with link to the recipe
recipe_link_element_list = soup.find_all('a', attrs={"class":"link d-block"})

#list holding information in dicts that will be put in database
data = list()

for element in recipe_link_element_list:

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
    
    #put everything into dict and put onto data list
    recipe = {
        'name' : name, 
        'ingredients' : ingredients, 
        'time' : time,
        'level' : level,
        'method' : method,
        'image' : image,
        'url' : recipe_url
        }
    
    data.append(recipe)

print(data)


# cur.execute("""
#     INSERT INTO recipe VALUES
#         
# """)


