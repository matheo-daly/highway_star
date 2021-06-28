from highway_star.scrapping.wikipedia_scraper import scrap_wikipedia_structure_with_content
from highway_star.preprocessing.biography_preprocessor import sent_to_words
from highway_star.preprocessing.biography_preprocessor import remove_stop_words_from_biographies
from highway_star.visualizing.visualizer import give_sankey_data_from_prefixspan
from highway_star.visualizing.visualizer import sankey_diagram_with_prefixspan_output
import pandas as pd


def run(root_category: str, lang: str, custom_stop_words: list, use_lemmatization: bool = False,
        allowed_postags: list = ['NOUN', 'VERB'], prefixspan_minlen: int = 10, prefixspan_topk: int = 50,
        js_filename: str = "sankey", html_filename: str = "index", title: str = "sankey"):
    content = scrap_wikipedia_structure_with_content(root_category=root_category, lang=lang)
    dataframe_with_biographies = pd.DataFrame.from_dict(content)
    dataframe_with_biographies["biographies_tokenized"] = sent_to_words(
        biographies_column=dataframe_with_biographies["content"])
    dataframe_with_biographies["biographies_cleaned"] = remove_stop_words_from_biographies(
        biographies_column=dataframe_with_biographies["biographies_tokenized"], custom_stop_words=custom_stop_words,
        use_lemmatization=use_lemmatization, allowed_postags=allowed_postags)
    sankey_data_from_prefixspan = give_sankey_data_from_prefixspan(
        data_tokenized=dataframe_with_biographies["biographies_cleaned"], prefixspan_minlen=prefixspan_minlen,
        prefixspan_topk=prefixspan_topk)
    sankey_diagram_with_prefixspan_output(sankey_data_from_prefixspan=sankey_data_from_prefixspan,
                                          js_filename=js_filename, html_filename=html_filename, title=title)
