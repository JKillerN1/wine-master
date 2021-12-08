import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler
import os.path

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('template.html')
date = int(os.path.split(os.path.split(str(datetime.datetime.now().date()).replace('-', '/'))[0])[0])

excel_data_df = pandas.read_excel('wine3.xlsx',
                                  sheet_name='Лист1',
                                  usecols=['Категория', 'Название', 'Сорт', 'Цена', 'Картинка', 'Акция'],
                                  na_values=['N/A', 'NA'], keep_default_na=False)
table = excel_data_df.to_dict(orient='records')
category_products = defaultdict(list)

for drink in table:
    category_products[drink["Категория"]].append(drink)
    rendered_page = template.render(
        date=date - 1920,
        category_products=category_products,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
