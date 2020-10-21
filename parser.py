import requests
import csv
from bs4 import BeautifulSoup
from multiprocessing import Pool


URL = 'https://coinmarketcap.com/all/views/all/'


# Function to retrieve html of the web page
def get_html(url, params=None, headers=None):
    r = requests.get(url, params=params, headers=headers) 
    return r.text										


# Function to retrieve all corresponding links on the web page
def get_all_links(html_code):
    soup = BeautifulSoup(html_code, 'lxml')
    tables = soup.find_all('tr', class_='cmc-table-row')
    links = []
    for tbl in tables:
        link = 'https://coinmarketcap.com' + tbl.find('a', class_='cmc-link').get('href')
        links.append(link)

    return links


# Function to scrape&parse HTML content
def get_content(url, html_code):
    soup = BeautifulSoup(html_code, 'lxml')

    name = url.split('/')[4]

    try:
        price = soup.find('span', class_='cmc-details-panel-price__price').text
    except:
        price = ''
        
    try:
        price = price.replace(',', '.')
    except:
        pass
        
    try:
        change = soup.find(
            class_='cmc--change-negative cmc-details-panel-price__price-change').text
    except:
        change = 0
        
    data = {
        'Name': name,
        'Price': price,
        'Price Change Past 24 hours': change,
        'URL': url
    }
    
    print(name.upper(), 'has parsed')
    return data


def write_csv(data):
    with open('coinmarket.txt', 'a') as f:
        writer = csv.writer(f)
        to_write = data['Name'], data['Price'], data['Price Change Past 24 hours'], data['URL']
        print(to_write)
        writer.writerow((to_write))


def make_all(url):
    html = get_html(url)
    data = get_content(url, html)
    write_csv(data)
    print('Saved in csv file')


def main():
    html_ = get_html(URL)
    all_links = get_all_links(html_)

    # Takes about ~8 minutes
    # for url in all_links:
    #  	 html = get_html(url)
    #  	 data = get_content(url, html)
    #  	 write_csv(data)

    # Takes about ~10 seconds
    with Pool(40) as p:
        p.map(make_all, all_links)


if __name__ == '__main__':
    main()
