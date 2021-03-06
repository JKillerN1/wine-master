import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

import argparse
from collections import defaultdict

if __name__ == '__main__':
    winery_creation_year = 1920
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )

    template = env.get_template('template.html')

    date_now = datetime.datetime.now()
    parser = argparse.ArgumentParser(
        description='Создание сайта'
    )
    parser.add_argument('link', help='Введите название файла')
    xlsx_file_path = parser.parse_args().link

    drinks = pandas.read_excel(xlsx_file_path,
                               sheet_name='Лист1',
                               usecols=['Категория',
                                        'Название',
                                        'Сорт',
                                        'Цена',
                                        'Картинка',
                                        'Акция'],
                               na_values=['N/A', 'NA'],
                               keep_default_na=False).to_dict(orient='records')
    products_by_category = defaultdict(list)

    for drink in drinks:
        products_by_category[drink["Категория"]].append(drink)

    rendered_page = template.render(
        age=date_now.year - winery_creation_year,
        category_products=products_by_category,
    )

    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()
