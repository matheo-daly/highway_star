from scrapping.WikipediaScraper import *


def scrap_wikipedia_structure_with_content(root_category: str, start_tag: str, end_tag: str, lang: str):
    all_pages: dict = scrap_wikipedia_structure(subcategories=[root_category], lang=lang)
    all_pages_with_content: dict = get_content_from_all_pages(all_pages=all_pages, start_tag=start_tag, end_tag=end_tag)
    return all_pages_with_content
