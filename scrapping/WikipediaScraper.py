from bs4 import BeautifulSoup, ResultSet
import requests
import re
from rich.progress import track
from typing import List


def get_subcategories_names_from_category(category: str) -> List[str]:
    subcategories_names = []
    soup: BeautifulSoup = BeautifulSoup(requests.get('https://fr.wikipedia.org/wiki/Catégorie:' + category).content,
                                        "html.parser")
    category: BeautifulSoup = soup.findAll("div", {"class": "mw-category-generated"})[0]
    try:
        sub_categories: BeautifulSoup = category.findAll("div", {"id": "mw-subcategories"})[0].findAll(
            "div", {"class": "mw-content-ltr"})[0].findAll("a")
        for sub_category in sub_categories:
            subcategories_names.append(sub_category.get_text().replace(" ", "_"))
    except IndexError:
        pass
    return subcategories_names


def get_pages_from_category(category: str) -> dict:
    pages_names = []
    pages_links = []
    subcategory = []
    soup: BeautifulSoup = BeautifulSoup(requests.get('https://fr.wikipedia.org/wiki/Catégorie:' + category)
                                        .content, "html.parser")
    try:
        category_generated: BeautifulSoup = soup.findAll("div", {"class": "mw-category-generated"})[0]
        pages: BeautifulSoup = category_generated.findAll("div", {"id": "mw-pages"})[0].findAll(
            "div", {"class": "mw-content-ltr"})[0].findAll("a")
        for page in pages:
            pages_links.append("https://fr.wikipedia.org" + page["href"])
            pages_names.append(page.get_text().replace(" ", "_"))
            subcategory.append(category)
    except IndexError:
        pass
    pages_dictionary: dict = {"pages_links": pages_links, "pages_names": pages_names, "subcategory": subcategory}
    return pages_dictionary


def scrap_wikipedia_structure(subcategories: List[str], pages_dictionary: dict = None) -> dict:
    if subcategories:
        new_subcategories: List[str] = []
        for names in track(subcategories, description="scrapping " + str(len(subcategories)) + " subcategories"):
            new_subcategories.extend(get_subcategories_names_from_category(names))
            pages: dict = get_pages_from_category(names)
            pages_dictionary["pages_links"].extend(pages["pages_links"])
            pages_dictionary["pages_names"].extend(pages["pages_names"])
            pages_dictionary["subcategory"].extend(pages["subcategory"])
        return scrap_wikipedia_structure(subcategories=new_subcategories, pages_dictionary=pages_dictionary)
    else:
        return pages_dictionary


def get_biography_from_page_content(page_content: BeautifulSoup) -> str:
    biography: str = ""
    try:
        paragraphs_in_biography: ResultSet = BeautifulSoup(
            str(page_content)
                .split('<span class="mw-headline" id="Biographie">Biographie</span>')[1]
                .split('<h2>')[0], "html.parser") \
            .findAll("p")
        for paragraphs in paragraphs_in_biography:
            biography += re.sub(r'\[.*\]', '',
                                paragraphs
                                .get_text()
                                .replace("«", "« ")
                                .replace("»", " »")
                                .replace("\xa0", "")
                                .replace("\n", "")
                                .replace(".", " . ")
                                .replace(",", " , ")
                                .replace(";", " ; ")
                                .replace(":", " : "))
    except IndexError:
        biography: str = "no_biography"
    return biography


def get_biographies_from_all_pages(all_pages_links: List[str]) -> List[str]:
    biographies: List[str] = []
    for link in track(all_pages_links, description="Getting all biographies from pages"):
        page_content: BeautifulSoup = BeautifulSoup(requests.get(link).content, "html.parser")
        biographies.append(get_biography_from_page_content(page_content))
    return biographies
