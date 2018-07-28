import urllib2
from bs4 import BeautifulSoup

# Data/screen scraper from a bookstore web page.
# It looks for books with 5 star rating and prints data about their:
# - title
# - total number
# - total price
# - average price
#
# Author: Djordje Gavrilovic

number = 0
sum = 0

def doScraping(url):

    global number
    global sum

    # Query the website and return the html
    page = urllib2.urlopen(url)

    # Parse the html using beautiful soup
    soup = BeautifulSoup(page, 'html.parser')

    # Take out the <ol> with class 'row' - container for <article>s
    container = soup.find('ol', attrs={'class': 'row'})
    articles = container.find_all('article')

    for article in articles:
        if article.p['class'][1] == 'Five':
            print article.h3.a.get('title')
            price = article.find('p','price_color').text
            price = price[1:] # remove the pound sign at the begining of price
            sum = sum + float(price)
            number += 1

    # Dealing with pagination    
    if soup.find('li','next') != None:
        new_url = ''
        a_href = soup.find('ul','pager').find('li','next').a.get('href')
        urlx = url.split('/')
        urlx[6] = a_href
        for part in urlx:
            new_url += part + "/"
        new_url = new_url[:-1]
        doScraping(new_url) # calls itself and continues scraping with new_url

# Start the scraping and print the results
doScraping('http://books.toscrape.com/catalogue/category/books_1/index.html') # bookstore that wants to be scraped ;)
print '-------------------'
print ("book num: " + str(number))
print ("sum: " + str(sum))
print ("avg: " + str(sum/number))

