from highway_star.scrapping import WikipediaScraper
WikipediaScraper.scrap_wikipedia_structure_with_content(
    root_category="Sexual_abuse_victim_advocates",
    start_tag='<span class="mw-headline" id="Death">Death</span>',
    end_tag='<h2>',
    lang="eng")
wikipedia_scraper.scrap_wikipedia_structure_with_content(
    root_category="Suicide_par_pays",
    start_tag='<span class="mw-headline" id="Biographie">Biographie</span>',
    end_tag='<h2>',
    lang="fr")
