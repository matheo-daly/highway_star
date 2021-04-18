from typing import NoReturn

import pandas as pd
from pandas import DataFrame

from scrapping.WikipediaScraper import *


def process() -> NoReturn:
    root_category: List[str] = ["Mort_par_suicide"]

    all_pages: dict = scrap_wikipedia_structure(subcategories=root_category,
                                                pages_dictionary={"pages_links": [], "pages_names": [],
                                                                  "subcategory": []})
    all_pages["biographies"]: dict = get_biographies_from_all_pages(all_pages_links=all_pages["pages_links"])
    dataframe: DataFrame = pd.DataFrame.from_dict(all_pages)
    dataframe: DataFrame = dataframe[(dataframe["subcategory"].str.contains("suicid")) | (dataframe["subcategory"]
                                                                               .str.contains("Suicid"))]
    dataframe: DataFrame = dataframe[dataframe["biographies"] != "no_biography"]
    dataframe.to_csv("../")
