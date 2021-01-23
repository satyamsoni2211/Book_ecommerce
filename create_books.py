import os
import django
import re
from pprint import pprint
from urllib3 import disable_warnings
from urllib3.exceptions import InsecureRequestWarning

disable_warnings(InsecureRequestWarning)

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Book_Ecommerce.settings")

django.setup()

import random
from inventory.models import Book
from requests import Session
from concurrent.futures import ThreadPoolExecutor

session = Session()
session.verify = False
pattern = re.compile(r"\d+\.?\d{0,}")

res = session.get("https://s3-ap-southeast-1.amazonaws.com/he-public-data/books8f8fe52.json")
books = res.json()

resi = session.get("https://s3-ap-southeast-1.amazonaws.com/he-public-data/bookimage816b123.json")
images = resi.json()

pprint(books[0])
print(random.choice(images))


def create_books(book: Book):
    print(f"saving book {book}")
    book.save()


with ThreadPoolExecutor(max_workers=os.cpu_count()*3) as executor:
    executor.map(create_books,
                 [Book(**i, image=random.choice(images).get("Image")) for i in books if
                  re.match(pattern, str(i.get("average_rating")))])
