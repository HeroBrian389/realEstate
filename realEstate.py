#!/usr/bin/env python3.6
# coding: utf-8
from bs4 import BeautifulSoup
import sys
from urllib.request import Request, urlopen

#driver = webdriver.Firefox()

#List of lists to determind who has the best value
nameList = []
priceList = []
bedsList = []
valueList = []
linksList = []
realLinks = []

# The site taken from CMD arguments
prop_page = sys.argv[1]
finalPage = ''


gooleVar = ''
price = ''

# I declare different variables such as daft for daft.ie because they all have different setups webpage wise
# I want my program to be able to use anywhere so you just plug in any link you have and my program will recommend a better value house
def daft():


    #STARTING REAL FUNCTIONS
    def price(property_page):
        #Request the webpage
        req = Request(str(property_page))
        page = urlopen(req).read()

        # Parse it through BS
        soup = BeautifulSoup(page, 'html.parser')

        #Extract the info we want
        # smi-price-string is the id on the div we want the info on in the webpage
        dataWanted = soup.find('div', attrs={'id': 'smi-price-string'})

        #Remove junk
        # Converts it into text
        name = dataWanted.text.strip()

        # Append the price to the list of prices to compare value
        priceList.append(price)

        # If the program has run successfully then it will display the best value house's price
        if win == True:
            print('It costs', price)
    #################################################

    # This function displays what kind of house it is - be it an apartment, duplex or detached house
    nameList = []

    def typeHouse(property_page):
        #Request the webpage
        req = Request(str(property_page))
        page = urlopen(req).read()

        # Parse it through BS
        soup = BeautifulSoup(page, 'html.parser')
        typeOfHouse = ''

        # Extract the info about type of house
        dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

        #Remove junk
        name = dataWanted.text.strip().split()

        #Remove the first value as it is the same as the cost
        name.pop(0)

        # Removing more junk
        a = name[0]

        # There is an error with € in python so we need to get rid of it
        if (a[0] == '€'):
            a = name[0]
            name.pop(0)

        # Appending the type of house to the string to compare & contrast
        typeOfHouse += str(name[0])

        # If the program has run successfully we will show the winning house's type
        if win == True:
            print('It is a/an', typeHouse)

    #################################################

    # THIS HAS YET TO BE IMPLEMENTED TO AFFECT THE VALUE OF THE house
    # This function will get the amount of baths that it has
    def bathAmount(property_page):
        #Request the webpage
        req = Request(str(property_page))
        page = urlopen(req).read()

        # Parse it through BS
        soup = BeautifulSoup(page, 'html.parser')
        dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

        #Remove junk
        name = dataWanted.text.strip().split()
        if 'Bath' in name:
            bathNum = name[-5]
            if win == True:
                print('It has', name, 'baths')
    #################################################

    # This function gets the amount of beds in the property
    def bedAmount(property_page):

        #Request the webpage
        req = Request(str(property_page))
        page = urlopen(req).read()

        # Parse it through BS
        soup = BeautifulSoup(page, 'html.parser')

        # Extract the stuff we want from the 'div'
        dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

        #Remove junk
        name = dataWanted.text.strip().split()

        # The string gives a lot of junk but the second last value is the amount of beds the house has
        bedNum = name[-2]

        # There was a problem with lists so we assign a to bedNum[0] to get around it
        a = bedNum[0]

        # Remove €
        if (a[0] == '€'):
            a = name[0]
            name.pop(0)

        # Add the number of beds to a list to compare the values of the houses
        bedsList.append(bedNum)

        # If the program has run successfully then display the winning house's number of beds
        if win == True:
            print('It has', bedNum, 'beds')

    #################################################

    # Display the location of the houses
    # I am still working on weighting the different areas in Dublin to either increase or decrease the value of the house depending on where it is
    # Eg a house in Darndale would be devalued but a house in Ballsbridge would increase in value

    def location(property_page):

        #Request the webpage
        req = Request(str(property_page))
        page = urlopen(req).read()

        # Parse it through BS
        soup = BeautifulSoup(page, 'html.parser')

        dataWanted = soup.find('div', attrs={'class': 'smi-object-header'})

        #Search for the bit of the webpage with the address
        data = dataWanted.find('h1')
        name = dataWanted.text.strip().split()

        # strip the junk
        name1 = data.text.strip().split()
        i = ''
        for address in name1:
            i += address + ' '

        # Add the location to the list of the locations
        nameList.append(i)
        googleVar = name1

        # If the program had run successfully then it will display the best value house's locaiton
        if win == True:
            print(i, 'is the location')

    #################################################

    # Google Maps search for shops --NOT WORKING--
    def googleMaps():
        googleVar.pop(0)
        i = ''
        for a in googleVar:
            i += a + '+'
        i = i[:-1]
        page = 'https://www.google.com/search?q=shops+near+' +i

        #Request the webpage
        driver.get(page)

        # Try parse the webpage and then click on some elements to access the shops nearby
        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content,"html.parser")
        data = soup.findALl("div", attrs={"class":"ccBEnf"})
        for i in data:
            print(i)

#################################################

# The algorithm in its current state only takes the price and divides it by the number of beds then takes the lowest number and uses that as the best value
# The end goal is to incorporate other factors into the end value such as;
# 1. A weighted system where each area in dublin has a value and based on the location will increase/decrease the value
# 2. Shops, public facilities and schools nearby
# 3. Density of people in the area
# 4. Amount of open/unused space in the area
# 5. Square feet in the houses

def algorithm(property_page):

    #Request the webpage
    req = Request(str(property_page))
    page = urlopen(req).read()

    # Parse it through BS
    soup = BeautifulSoup(page, 'html.parser')

    # Extract what we want
    dataWanted = soup.find('ul', attrs={'class': 'smi-other'})

    #Search for the bit of the webpage with the address
    data = dataWanted.findAll('a')
    data = str(data)
    remove = data.split()

    # Create a list called links to add all of the other houses links onto
    links = []

    # Create a loop to remove the 'href' from the front of loops
    for link in remove:
        if (link[0] == 'h') and (link[1] == 'r'):
            # Remove the href from the start and quotes from the end of the link
            link = link[6:]
            link = link[:-2]

            # Once cleaned, add it onto the end of the link list
            links.append(link)
    # Add the original link to the list of links
    links.append(property_page[19:])

    # Duplicate the link list for future use
    linksList = links

    # Loop to use the link lists and run them through the functions
    for i in links:
        property_page = 'https://www.daft.ie' + i

        realLinks.append(property_page)

        # WILL BE ADDED TO IN THE FUUTRE
        price(property_page)
        typeHouse(property_page)
        bathAmount(property_page)
        bedAmount(property_page)
        location(property_page)

######################## #########################

# The analyse bit is just divide the value by the amount of beds
# Will be adding more factors as mentioned above

def analyse():

    # Declare global variables
    global valueList, finalPage

    # Create a baseline
    num = 0

    # While loop to loop until the amount of beds is equal to the baseline
    # Anlyse the priceList here as they are same length

    while (len(bedsList) > num):
        # Price is the first value of the priceList
        price = priceList[num]

        # Remove junk so price can become a float
        price = [item.replace("€", "") for item in price]
        price = [item.replace(",", "") for item in price]

        # Small loop to append each letter of the list onto a string to get a complete number that can be used as the price
        p = ''
        for x in price:
            p += x

        # Remove the last 2 values
        p = p[:-2]

        # Create the float
        priceReal = float(p)

        # Turn beds into a float
        beds = bedsList[num]
        beds = float(beds)

        # Do the division of price divided by beds
        value = priceReal / beds

        # Add the result onto the end of valueList to be compared
        valueList.append(value)

        # Incremnent the value of num to go onto the next value on priceList and bedsList
        num = num + 1

    # Sort the valueList in order of size
    tempValueList = valueList
    tempValueList.sort(key=int)

    # Get the position of the highest value and cross reference it with the original list
    # E.g. ['10', '3' ,'2', '1'] is the ordered list
    # ['1', '2', '10',' 3'] is the unordered list
    # We now know which linkList position it is as it is the same
    tempPos = valueList.index(tempValueList[0])

    # Print best value and at which value
    print(nameList[tempPos], 'is best value, at', value, 'per bed')

    # Get the position of the linkList to find out more about the best value house
    property_page = realLinks[tempPos]
    property_page = str(property_page)

    # Print more info about the house
    print('More info:', property_page)
    finalPage = property_page


#################################################
# Running functions
win = False
algorithm(prop_page)

# When the program has run it then 
win = True
analyse()
#################################################

property_page = finalPage
#Request the webpage
req = Request(str(property_page))
page = urlopen(req).read()

# Parse it through BS
soup = BeautifulSoup(page, 'html.parser')

#Extract the info we want
dataWanted = soup.find('div', attrs={'id': 'smi-price-string'})

#Remove junk
name = dataWanted.text.strip()
price = name
print('It costs', price)

#Request the webpage
req = Request(str(property_page))
page = urlopen(req).read()

# Parse it through BS
soup = BeautifulSoup(page, 'html.parser')
typeOfHouse = ''
# Extract the info about type of house
dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

#Remove junk
name = dataWanted.text.strip().split()

#Remove the first value as it is the same as the cost
name.pop(0)

# Removing more junk
a = name[0]
if (a[0] == '€'):
    a = name[0]
    name.pop(0)

typeHouse = name[0]
print('It is a/an', typeHouse)

#Request the webpage
req = Request(str(property_page))
page = urlopen(req).read()

# Parse it through BS
soup = BeautifulSoup(page, 'html.parser')
dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

#Remove junk
name = dataWanted.text.strip().split()
if 'Bath' in name:
    bathNum = name[-5]
    print('It has', name, 'baths')

dataWanted = soup.find('div', attrs={'id': 'smi-summary-items'})

#Remove junk
name = dataWanted.text.strip().split()

bedNum = name[-2]
bedsList.append(bedNum)
print('It has', bedNum, 'beds')
