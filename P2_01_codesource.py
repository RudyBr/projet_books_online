from bs4 import BeautifulSoup
import requests
import csv
import re


# recherche des informations d'un livre et écriture sur un fichier .csv au nom de la catégorie
def infos_livre(book_url):
    page = requests.get(book_url)
    soup = BeautifulSoup(page.content, "html.parser")
    # initialisation de la liste qui recevra les informations du livre
    informations_livre = []
    # récupération url du livre
    product_page_url = book_url
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
    product_description = soup.find("article", {"class": "product_page"}).find("p", {"class": False})
    # vérification de la présence d'une description
    if product_description:
        product_description = soup.find("article", {"class": "product_page"}).find("p", {"class": False}).text
    else:
        product_description = "Pas de description"
    # Récupération de la catégorie du livre
    book_category = (soup.find("a", href=re.compile("../category/books/"))).text
    # dictionnaire aidant à transformer les données rating lettrées en données chiffrées
    trans_chiffre = {"One": "1", "Two": "2", "Three": "3", "Four": "4", "Five": "5"}
    # Récupération de la note du livre
    review_rating_ext = soup.find("p", class_=re.compile("star-rating")).attrs
    review_rating = (trans_chiffre[review_rating_ext["class"][1]]) + " étoile(s) sur 5"
    # Récupération de l'url de l'image du livre
    image_url_ext = soup.find("img").attrs
    image_url = image_url_ext["src"].replace("../../", site_url)
    informations_livre.extend([product_page_url, upc, title, price_including_tax, price_excluding_tax, number_available,
                               product_description, book_category, review_rating, image_url])
    # ouverture du fichier .csv de la catégorie actuelle en mode ajout pour écrire les informations du livre
    with open(f"{book_category}.csv", "a", encoding="utf-8", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=";")
        writer.writerow(informations_livre)


# parcours des liens de tous les livres d'une page afin de boucler dessus
def links_books_extraction(url_des_categories):
    books_page = requests.get(url_des_categories)
    books_soup = BeautifulSoup(books_page.content, "html.parser")
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
           "universal_product code (upc)",
           "title",
           "price_including_tax",
           "price_excluding_tax",
           "number_available",
           "product_description",
           "category",
           "review_rating",
           "image_url"]

site_url = "http://books.toscrape.com/"
url = "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
all_category_response = requests.get(site_url)
all_category_soup = BeautifulSoup(all_category_response.content, "html.parser")
# création d'une liste afin de récupérer chaque suffixe de chaque page de catégorie
categories = all_category_soup.findAll("a", href=re.compile("catalogue/category/books/"))
# récupération du nombre de catégories pour itérer dessus
for i in range(len(categories)):
    # concaténation de l'adresse du site avec le suffixe d'adresse de catégorie
    category_url = site_url + categories[i].attrs["href"]
    # vérification de l'existence d'une page avec le suffixe /page-1.html de la catégorie
    if requests.get(category_url.replace("/index.html", "/page-1.html")).ok:
        category_page = requests.get(category_url)
        category_soup = BeautifulSoup(category_page.content, "html.parser")
        # récupération information page 1 sur x
        current_page = category_soup.find("li", class_="current").text
        # création du nom fichier nom_de_la_catégorie.csv
        category_csv = category_soup.find("div", class_="page-header action").find("h1").text + ".csv"
        # création du fichier .csv de la catégorie et écriture de l'en-tête
        with open(category_csv, "w", newline="", encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv, delimiter=";")
            writer.writerow(en_tete)
        # itération sur les caractères de l'information 1 sur x
        for caractere in current_page:
            # vérification si le caractère est différent de 1 et est un chiffre afin de récupérer le nombre de pages
            if caractere != "1" and caractere.isdigit():
                # itération afin de parcourir les diférentes pages de la catégorie
                for j in range(1, int(caractere) + 1):
                    category_urls = category_url.replace("/index.html", "/page-" + str(j) + ".html")
                    links_books_extraction(category_urls)
    # Si absence page avec le suffixe /page-1.html, la catégorie ne possède qu'une page
    else:
        category_page = requests.get(category_url)
        category_soup = BeautifulSoup(category_page.content, "html.parser")
        category_csv = category_soup.find("div", class_="page-header action").find("h1").text + ".csv"
        with open(category_csv, "w", newline="", encoding="utf-8") as file_csv:
            writer = csv.writer(file_csv, delimiter=";")
            writer.writerow(en_tete)
        links_books_extraction(category_url)
