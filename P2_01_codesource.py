from bs4 import BeautifulSoup
import requests
import csv
import re

# lien de la page à parser
site_url = "http://books.toscrape.com/"
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
page = requests.get(url)
en_tete = ["product_page_url",
           "universal_product code (upc)",
           "title",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "product_description",
           "category",
           "review_rating",
           "image_url"]

soup = BeautifulSoup(page.content, "html.parser")

# dictionnaire pour transformer données rating lettrées en données chiffrées
Trans_chiffre = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}

informations_livre = []
# récupération url du livre
product_page_url = url
# Récupération UPC du livre
upc = (soup.find("th", text="UPC").find_next_sibling("td")).text
# Récupération titre du livre
title = (soup.find("div", {"class": "col-sm-6 product_main"}).find("h1")).text
# Récupération prix taxé
price_including_tax = (soup.find("th", text="Price (incl. tax)").find_next_sibling("td")).text
# Récupération prix hors taxe
price_excluding_tax = (soup.find("th", text="Price (excl. tax)").find_next_sibling("td")).text
# Récupération nombre de livres disponibles
number_available = "".join([ele for ele
                            in soup.find("th", text="Availability").find_next_sibling("td").text
                            if ele.isdigit()])
# Récupération de la description du livre
product_description = (soup.find("article", {"class": "product_page"}).find("p", {"class": False})).text
# Récupération de la catégorie du livre
category = (soup.find("a", href=re.compile("../category/books/"))).text
# Récupération de la note du livre
review_rating_ext = soup.find("p", class_=re.compile("star-rating")).attrs
review_rating = Trans_chiffre[review_rating_ext["class"][1]]
# Récupération de l'url de l'image du livre
image_url_ext = soup.find("img").attrs
image_url = image_url_ext["src"].replace("../../", site_url)

informations_livre.extend([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                           product_description, category,review_rating, image_url])

print(informations_livre)

with open("data.csv", "w", encoding="utf-8", newline="") as data_csv:
    writer = csv.writer(data_csv, delimiter=";")
    writer.writerow(en_tete)
    writer.writerow(informations_livre)
