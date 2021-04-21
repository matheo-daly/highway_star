from bs4 import BeautifulSoup, ResultSet
import requests
import re
from rich.progress import track
from typing import List


def get_subcategories_names_from_category(category: str, lang: str) -> List[str]:
    subcategories_names = []
    category_root = ""
    if lang == "fr":
        category_root = 'https://fr.wikipedia.org/wiki/Catégorie:'
    elif lang == "eng":
        category_root = 'https://en.wikipedia.org/wiki/Category:'
    soup: BeautifulSoup = BeautifulSoup(requests.get(category_root + category).content,
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


def get_pages_from_category(category: str, lang: str) -> dict:
    pages_names = []
    pages_links = []
    subcategory = []
    category_root = ""
    wikipedia_root = ""
    if lang == "fr":
        category_root = 'https://fr.wikipedia.org/wiki/Catégorie:'
        wikipedia_root = "https://fr.wikipedia.org"
    elif lang == "eng":
        category_root = 'https://en.wikipedia.org/wiki/Category:'
        wikipedia_root = "https://en.wikipedia.org/wiki/"
    soup: BeautifulSoup = BeautifulSoup(requests.get(category_root + category)
                                        .content, "html.parser")
    try:
        category_generated: BeautifulSoup = soup.findAll("div", {"class": "mw-category-generated"})[0]
        pages: BeautifulSoup = category_generated.findAll("div", {"id": "mw-pages"})[0].findAll(
            "div", {"class": "mw-content-ltr"})[0].findAll("a")
        for page in pages:
            pages_links.append(wikipedia_root + page["href"])
            pages_names.append(page.get_text().replace(" ", "_"))
            subcategory.append(category)
    except IndexError:
        pass
    pages_dictionary: dict = {"pages_links": pages_links, "pages_names": pages_names, "subcategory": subcategory}
    return pages_dictionary


def scrap_wikipedia_structure(subcategories: List[str], lang: str,
                              pages_dictionary: dict = {"pages_links": [], "pages_names": [],
                                                        "subcategory": []}) -> dict:
    if subcategories:
        new_subcategories: List[str] = []
        for names in track(subcategories, description="scrapping " + str(len(subcategories)) + " subcategories"):
            new_subcategories.extend(get_subcategories_names_from_category(names, lang))
            pages: dict = get_pages_from_category(names, lang)
            pages_dictionary["pages_links"].extend(pages["pages_links"])
            pages_dictionary["pages_names"].extend(pages["pages_names"])
            pages_dictionary["subcategory"].extend(pages["subcategory"])
        return scrap_wikipedia_structure(subcategories=new_subcategories, pages_dictionary=pages_dictionary, lang=lang)
    else:
        return pages_dictionary


def get_specific_content_from_page(page_content: BeautifulSoup, start_tag: str, end_tag: str) -> str:
    biography: str = ""
    try:
        paragraphs_in_biography: ResultSet = BeautifulSoup(
            str(page_content)
                .split(start_tag)[1]
                .split(end_tag)[0], "html.parser") \
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
        biography: str = "no_matching_content"
    return biography


def get_content_from_all_pages(all_pages: dict, start_tag: str, end_tag: str) -> dict:
    content: List[str] = []
    for link in track(all_pages["pages_links"], description="Getting all content from pages"):
        page_content: BeautifulSoup = BeautifulSoup(requests.get(link).content, "html.parser")
        content.append(get_specific_content_from_page(
            page_content=page_content,
            start_tag=start_tag,
            end_tag=end_tag))
    all_pages["content"] = content
    return all_pages


def scrap_wikipedia_structure_with_content(root_category: str, start_tag: str, end_tag: str, lang: str):
    all_pages: dict = scrap_wikipedia_structure(subcategories=[root_category], lang=lang)
    all_pages_with_content: dict = get_content_from_all_pages(all_pages=all_pages, start_tag=start_tag, end_tag=end_tag)
    return all_pages_with_content
