import requests
from bs4 import BeautifulSoup
import json
import time

def get_book_urls(id):
    url = f'https://daraladab.net/allbooks.php?page={id}'
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
              }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
        exit()
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find elements using CSS selectors or other methods
    #   For example, let's say you want to extract all the links on the page:
    links = soup.find_all('a')

    # Specify the path where you want to save the JSON data
    output_file_path = 'scraped_data.json'
    hrefs=list(set([item.get('href') for item in links if "book.php?id=" in item.get('href')]))

    json_data = json.dumps(hrefs, indent=4)

    # Write the JSON data to the file
    with open(output_file_path, 'a') as output_file:
        output_file.write(json_data)

    time.sleep(3)

def get_book_info(url):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
              }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
        exit()
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find elements using CSS selectors or other methods
    soup = BeautifulSoup(html_content, 'html.parser',from_encoding='utf-8')
    product_detail_div = soup.find('div', class_='single-product-detail')
    
    bookname=product_detail_div.find('h3').get_text(strip=True)
    description=[paragraph.get_text(strip=True) for paragraph in product_detail_div.find('div',class_='description').find_all('p')]
    description=' '.join(description)
    moredata=product_detail_div.find('div', class_='book-info-list').find('ul').find_all('li')
    authorname=moredata[0].find('a').get_text(strip=True)
    ISBN=moredata[1].get_text().split(':')[1]
    CoverType=moredata[2].get_text().split(':')[1]
    PagesNumber=moredata[3].get_text().split(':')[1]
    Price=moredata[4].get_text().split(':')[1]
    Size=moredata[5].get_text().split(':')[1]
    Weight=moredata[6].get_text().split(':')[1]
    PublishDate=moredata[7].get_text().split(':')[1]
    book={
        "url":url,
        "Bookname":bookname,
        "description":description,
        "authorname":authorname,
        "ISBN":ISBN,
        "CoverType":CoverType,
        "PagesNumber":PagesNumber,
        "Price":Price,
        "Size":Size,
        "Weight":Weight,
        "PublishDate":PublishDate}
    time.sleep(1)
    print("Book Taken")
    print(book)
    return book

def get_book_info_translator(url):
    
    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
              }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        html_content = response.content
    else:
        print("Failed to retrieve the webpage")
        exit()
    # Create a BeautifulSoup object
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find elements using CSS selectors or other methods
    soup = BeautifulSoup(html_content, 'html.parser',from_encoding='utf-8')
    product_detail_div = soup.find('div', class_='single-product-detail')
    
    bookname=product_detail_div.find('h3').get_text(strip=True)
    description=[paragraph.get_text(strip=True) for paragraph in product_detail_div.find('div',class_='description').find_all('p')]
    description=' '.join(description)
    moredata=product_detail_div.find('div', class_='book-info-list').find('ul').find_all('li')
    authorname=moredata[0].find('a').get_text(strip=True)
    ISBN=moredata[2].get_text().split(':')[1]
    CoverType=moredata[3].get_text().split(':')[1]
    PagesNumber=moredata[4].get_text().split(':')[1]
    Price=moredata[5].get_text().split(':')[1]
    Size=moredata[6].get_text().split(':')[1]
    Weight=moredata[7].get_text().split(':')[1]
    PublishDate=moredata[8].get_text().split(':')[1]
    TranslatorName=moredata[0].get_text().split(':')[1]
    book={
        "url":url,
        "Bookname":bookname,
        "description":description,
        "authorname":authorname,
        "ISBN":ISBN,
        "CoverType":CoverType,
        "PagesNumber":PagesNumber,
        "Price":Price,
        "Size":Size,
        "Weight":Weight,
        "PublishDate":PublishDate,
        "Translator":TranslatorName}
    time.sleep(1)
    print("Book Taken")
    print(book)
    return book
    

# # Getting all books urls.
# [get_book_urls(id) for id in list(range(1, 40))] 

# #Removing Duplicates
# with open('scraped_data.json', 'r') as input_file:
#     links = json.load(input_file)

# links = list(set(links))

# with open('scraped_data.json', 'w') as output_file:
#     json.dump(links, output_file, indent=4)

#GettingBookInfo
with open('scraped_data.json', 'r') as input_file:
    links= json.load(input_file)
with open('Books.json', 'r') as input_file:
    booksloaded= json.load(input_file)

# Extract existing URLs from loaded books
existing_urls = [book['url'] for book in booksloaded]

# Find new links that haven't been loaded
new_links = [link for link in links if link not in existing_urls]

#For books who have a translator
new_books = [get_book_info_translator(link) for link in new_links]

# # Fetch book info for new links
# new_books = [get_book_info(link) for link in new_links]

# Add new books to the existing loaded data
booksloaded.extend(new_books)

# Save the updated data back to 'Books.json'
with open('Books.json', 'w') as output_file:
    json.dump(booksloaded, output_file, indent=4)




