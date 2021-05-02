from prefixspan import PrefixSpan
from time import time
import pandas
from rich.progress import track


def give_sankey_data_from_prefixspan(data_lemmatized: pandas.core.series.Series,
                                     prefixspan_minlen=10,
                                     prefixspan_topk=50) -> object:
    t = time()
    print("Executing Prefixspan...")
    prefixspan_initialized = PrefixSpan(data_lemmatized)
    prefixspan_initialized.minlen = prefixspan_minlen
    top_50 = prefixspan_initialized.topk(prefixspan_topk)
    print('Time to execute prefixspan: {} min'.format(round((time() - t) / 60, 2)))

    all_combinations = []
    for array in track(top_50, description="Process sankey data from prefixspan"):
        for i in range(len(array[1])):
            try:
                number_of_elements = 0
                words = []
                if array[1][i] != array[1][i + 1]:
                    words = [array[1][i], array[1][i + 1]]
                    for j in range(len(top_50)):
                        ponderer = top_50[j][0]
                        for k in range(len(top_50[j][1])):
                            if top_50[j][1][k] == words[0] and top_50[j][1][k + 1] == words[1]:
                                number_of_elements += ponderer
                    words.append(number_of_elements)
                    all_combinations.append(words)
            except IndexError:
                pass

    return pandas.DataFrame(all_combinations).drop_duplicates().values.tolist()


def write_js(sankey_data: list, title: str) -> str:
    beginning_js = """Highcharts.chart('container', {

        title: {
            text: '"""+title+"""'
        },
        accessibility: {
            point: {
                valueDescriptionFormat: '{index}. {point.from} to {point.to}, {point.weight}.'
            }
        },
        series: [{
            keys: ['from', 'to', 'weight'],
            data: """
    end_js = """,
            type: 'sankey',
            name: 'Sankey demo series'
        }]

    });"""
    return beginning_js + str(sankey_data) + end_js


def write_html(title: str, js_filename: str) -> str:
    return """<!doctype html><html lang="en"><head><meta charset="utf-8"><title>""" + title + """</title>
  <meta name="description" content="The HTML5 Herald">
  <meta name="author" content="SitePoint">
  <script src="https://code.highcharts.com/highcharts.js"></script>
  <script src="https://code.highcharts.com/modules/sankey.js"></script>
  <script src="https://code.highcharts.com/modules/exporting.js"></script>
  <script src="https://code.highcharts.com/modules/export-data.js"></script>
  <script src="https://code.highcharts.com/modules/accessibility.js"></script> 
</head>
<body>
<figure class="highcharts-figure">
  <div id="container"><script src='""" + js_filename + """.js'></script></div>
</figure>
</body>
</html>"""


def sankey_diagram_with_prefixspan_output(sankey_data_from_prefixspan: list, js_filename="data", html_filename="page",
                                          title=None):
    if title is None:
        title = html_filename
    text_file = open(js_filename+".js", "w")
    n = text_file.write(write_js(sankey_data_from_prefixspan, title=title))
    text_file.close()
    print("js file written successfully !")
    text_file = open(html_filename + ".html", "w")
    n = text_file.write(write_html(html_filename, js_filename))
    text_file.close()
    print("html file written successfully !")
