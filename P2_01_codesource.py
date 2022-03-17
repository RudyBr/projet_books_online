from pathlib import Path
from bs4 import BeautifulSoup
import requests
import csv
import re
import urllib.request


# recherche des informations d'un livre et écriture sur un fichier .csv au nom de la catégorie
def infos_livre(book_url):
    page = requests.get(book_url)
    book_soup = BeautifulSoup(page.content, "html.parser")
    # initialisation de la liste qui recevra les informations du livre
    informations_livre = []
    # récupération url du livre
    product_page_url = book_url
    # Récupération UPC du livre
    upc = (book_soup.find("th", text="UPC").find_next_sibling("td")).text
    # Récupération titre du livre
    title = (book_soup.find("div", {"class": "col-sm-6 product_main"}).find("h1")).text
    # Récupération prix taxé
    price_including_tax = (book_soup.find("th", text="Price (incl. tax)").find_next_sibling("td")).text
    # Récupération prix hors taxe
    price_excluding_tax = (book_soup.find("th", text="Price (excl. tax)").find_next_sibling("td")).text
    # Récupération nombre de livres disponibles
    number_available = "".join([ele for ele
                                in book_soup.find("th", text="Availability").find_next_sibling("td").text
                                if ele.isdigit()])
    # Récupération de la description du livre
    product_description = book_soup.find("article", {"class": "product_page"}).find("p", {"class": False})
    # vérification de la présence d'une description
    if product_description:
        product_description = book_soup.find("article", {"class": "product_page"}).find("p", {"class": False}).text
    else:
        product_description = "Pas de description"
    # Récupération de la catégorie du livre
    book_category = (book_soup.find("a", href=re.compile("../category/books/"))).text
    # dictionnaire aidant à transformer les données rating lettrées en données chiffrées
    trans_chiffre = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    # Récupération de la note du livre
    review_rating_ext = book_soup.find("p", class_=re.compile("star-rating")).attrs
    review_rating = (trans_chiffre[review_rating_ext["class"][1]]) + " étoile(s) sur 5"
    # Récupération de l'url de l'image du livre
    image_url_ext = book_soup.find("img").attrs
    image_url = image_url_ext["src"].replace("../../", site_url)
    informations_livre.extend([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                               product_description, book_category, review_rating, image_url])
    # ouverture du fichier .csv de la catégorie actuelle en mode append pour écrire les informations du livre
    with open(category_csv, "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(informations_livre)

    image_title = book_url.replace(book_url[book_url.find("_"):], ".jpg").replace(
        "http://books.toscrape.com/catalogue/", "").replace("-", "_")
    urllib.request.urlretrieve(image_url, category_repertory + image_title)


# parcours des liens de tous les livres d'une page afin de boucler dessus
def links_books_extraction(books_soup):
    # récupération de tous les suffixes d'adresse de livres de la page dans une liste
    book_links = books_soup.findAll("h3")
    # boucle parcourant la liste de suffixe de liens des livres pour les modifier et les inscrire dans le fichier.csv
    for h3 in book_links:
        a = h3.find("a")
        link = a["href"]
        # transformation des suffixes récupérés en liens valides, vers les adresses de livre
        book_url = link.replace("../../../", site_url + "catalogue/")
        infos_livre(book_url)


# liste des informations demandées servant d'en-tête
en_tete = ["product_page_url",
           "universal_product_code_(upc)",
           "title",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "product_description",
           "category",
           "review_rating",
           "image_url"]

site_url = "http://books.toscrape.com/"
all_category_response = requests.get(site_url)
all_category_soup = BeautifulSoup(all_category_response.content, "html.parser")
# création d'une liste afin de récupérer chaque suffixe de chaque page de catégorie
categories = all_category_soup.findAll("a", href=re.compile("catalogue/category/books/"))
# récupération du nombre de catégories pour itérer dessus
for category in categories:

    # concaténation de l'adresse du site avec le suffixe d'adresse de catégorie
    category_url = site_url + category.attrs["href"]
    # vérification de l'existence d'une page avec le suffixe /page-1.html de la catégorie
    request = requests.get(category_url)
    soup_list = [BeautifulSoup(request.content, "html.parser")]
    pageInt = 2

    # Si une page 2 de la catégorie existe, on ajoute des objet Beautifulsoup des pages 2 à x de la catégorie
    while True:
        request = requests.get(category_url.replace("/index.html", "/page-" + str(pageInt) + ".html"))
        pageInt += 1
        if request.ok:
            soup_list.append(BeautifulSoup(request.content, "html.parser"))
        else:
            break
    # Récupération du nom de la catégorie
    category_name = soup_list[0].find("div", class_="page-header action").find("h1").text
    # Création d'un dossier pour la catégorie actuelle
    Path(f"./{category_name}").mkdir()
    category_repertory = "./" + category_name + "/"
    category_csv = category_repertory + category_name + ".csv"
    print(f"Extraction des données de la catégorie: {Path(category_csv).stem}")
    # Création du fichier .csv de la catégorie actuelle et écriture de la ligne d'en-tête
    fichier_csv = Path(category_csv)
    fichier_csv.write_text("; ".join(en_tete) + "\n")

    for soup in soup_list:
        links_books_extraction(soup)
