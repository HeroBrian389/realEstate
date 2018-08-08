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


        name1 = data.text.strip().split()
        i = ''
        for address in name1:
            i += address + ' '

        nameList.append(i)
        googleVar = name1
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

        content = driver.page_source.encode('utf-8').strip()
        soup = BeautifulSoup(content,"html.parser")
        data = soup.findALl("div", attrs={"class":"ccBEnf"})
        for i in data:
            print(i)

#################################################

def algorithm(property_page):

    #Request the webpage
    req = Request(str(property_page))
    page = urlopen(req).read()

    # Parse it through BS
    soup = BeautifulSoup(page, 'html.parser')

    dataWanted = soup.find('ul', attrs={'class': 'smi-other'})

    #Search for the bit of the webpage with the address
    data = dataWanted.findAll('a')
    data = str(data)
    remove = data.split()

    links = []
    for link in remove:
        if (link[0] == 'h') and (link[1] == 'r'):
            link = link[6:]
            link = link[:-2]
            links.append(link)
    links.append(property_page[19:])

    linksList = links

    for i in links:
        property_page = 'https://www.daft.ie' + i
        realLinks.append(property_page)
        price(property_page)
        typeHouse(property_page)
        bathAmount(property_page)
        bedAmount(property_page)
        location(property_page)

######################## #########################
def analyse():
    global valueList, finalPage
    num = 0
    while (len(bedsList) > num):
        price = priceList[num]

        price = [item.replace("€", "") for item in price]
        price = [item.replace(",", "") for item in price]
        p = ''
        for x in price:
            p += x

        p = p[:-2]
        priceReal = float(p)
        beds = bedsList[num]
        beds = float(beds)

        value = priceReal / beds
        valueList.append(value)
        num = num + 1

    tempValueList = valueList
    tempValueList.sort(key=int)

    tempPos = valueList.index(tempValueList[0])

    print(nameList[tempPos], 'is best value, at', value, 'per bed')

    property_page = realLinks[tempPos]
    property_page = str(property_page)
    print('More info:', property_page)
    finalPage = property_page


#################################################
# Running functions
win = False
algorithm(prop_page)

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
