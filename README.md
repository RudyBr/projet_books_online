# projet_books_online
Projet 02 de la formation Développeur d'applications: Python

Fichier : P2_01_codesource.py

Script développé avec Python 3.9.

Ce sript permet d'extraire les données des livres du site http://books.toscrape.com/ pour les inscrire dans un fichier .csv. 
Il permet par ailleurs de récupérer les images des couvertures au format .jpg.
Ces fichiers seront organisés dans des dossiers nommés par catégorie. Ces derniers seront réunis dans le dossier Extraction généré par le script.

**Informations contenues par le fichier .csv:**
- product_page_url
- universal_product_code (upc)
- title
- price_including_tax
- price_excluding_tax
- number_available
- product_description
- category
- review_rating
- image_url

___

### Installation de l'environnement virtuel:

### Sous Windows :

Créer un dossier, afin d'y déposer le script et installer l'environnement virtuel.

**Dans l'invite de commande:**

Se placer dans le dossier du script, puis créer le dossier d'environnement avec la commande:

```
python -m venv env
```
Activez l'environnement:
```
\env\Scripts\activate.bat
```
Installez les packages nécessaires au fonctionnement du script:
Disposez le fichier requirements.txt au côté du dossier env, précédemment créé.
```
pip install -r requirements.txt
```
Lancement du script:
```
python P2_01_codesource.py
```


### Sous Unix (Linux/Mac OS) :

Créer un dossier, afin d'y déposer le script et installer l'environnement virtuel.

**Dans le terminal:**

Se placer dans le dossier du script, puis créer le dossier d'environnement avec la commande:

```
python -m venv env
```
Activez l'environnement:
```
source env/bin/activate
```
Installez les packages nécessaires au fonctionnement du script:
Disposez le fichier requirements.txt au côté du dossier env, précédemment créé.
```
pip install -r requirements.txt
```
Lancement du script:
```
python P2_01_codesource.py
```
