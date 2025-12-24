import json
from mongoengine import connect
from models import Author, Quote

DB_URI = "mongodb+srv://<USER>:<Bohdan1>@<CLUSTER>.mongodb.net/<DB_NAME>?retryWrites=true&w=majority"
connect(host=DB_URI)

def load_data():
    with open('authors.json', 'r', encoding='utf-8') as f:
        authors_list = json.load(f)
        
    for author_data in authors_list:
        if not Author.objects(fullname=author_data['fullname']):
            Author(**author_data).save()
    
    print("Authors uploaded successfully.")

    with open('quotes.json', 'r', encoding='utf-8') as f:
        quotes_list = json.load(f)
        
    for quote_data in quotes_list:
        author_name = quote_data['author']
        author = Author.objects(fullname=author_name).first()
        
        if author:
            if not Quote.objects(quote=quote_data['quote']):
                Quote(
                    tags=quote_data['tags'],
                    author=author,
                    quote=quote_data['quote']
                ).save()
                
    print("Quotes uploaded successfully.")

if __name__ == '__main__':
    load_data()