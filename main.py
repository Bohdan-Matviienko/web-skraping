import json
import requests
from bs4 import BeautifulSoup

BASE_URL = 'http://quotes.toscrape.com'

def get_author_details(author_url):
    response = requests.get(BASE_URL + author_url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    author_details = soup.find('div', class_='author-details')
    
    # Витягуємо дані відповідно до полів моделі Author з ДЗ #8
    fullname = author_details.find('h3', class_='author-title').get_text(strip=True)
    born_date = author_details.find('span', class_='author-born-date').get_text(strip=True)
    born_location = author_details.find('span', class_='author-born-location').get_text(strip=True)
    description = author_details.find('div', class_='author-description').get_text(strip=True)
    
    return {
        "fullname": fullname,
        "born_date": born_date,
        "born_location": born_location,
        "description": description
    }

def main():
    quotes_data = []
    authors_data = []
    seen_authors = set()
    
    page = 1
    while True:
        url = f'{BASE_URL}/page/{page}/'
        print(f'Scraping page {page}...')
        
        response = requests.get(url)
        if "No quotes found!" in response.text:
            break
            
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')
        
        if not quotes:
            break
            
        for quote in quotes:
            text = quote.find('span', class_='text').get_text(strip=True)
            author_name = quote.find('small', class_='author').get_text(strip=True)
            tags = [tag.get_text(strip=True) for tag in quote.find_all('a', class_='tag')]
            
            # Зберігаємо цитату (структура для quotes.json з ДЗ #8)
            quotes_data.append({
                "tags": tags,
                "author": author_name,
                "quote": text
            })
            
            # Обробка автора
            author_link = quote.find('a', href=True)['href']
            if author_link not in seen_authors:
                print(f"  Fetching info for: {author_name}")
                try:
                    author_info = get_author_details(author_link)
                    authors_data.append(author_info)
                    seen_authors.add(author_link)
                except Exception as e:
                    print(f"Error scraping author {author_name}: {e}")
        
        next_btn = soup.find('li', class_='next')
        if not next_btn:
            print("No next page. Finished.")
            break
            
        page += 1
    with open('quotes.json', 'w', encoding='utf-8') as f:
        json.dump(quotes_data, f, ensure_ascii=False, indent=2)
        
    with open('authors.json', 'w', encoding='utf-8') as f:
        json.dump(authors_data, f, ensure_ascii=False, indent=2)

    print("Data scraped and saved to json files.")

if __name__ == '__main__':
    main()