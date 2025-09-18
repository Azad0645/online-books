import os
from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader
import json


BOOKS_PER_PAGE = 20


def render():
    with open('meta_data.json', encoding='utf-8') as my_file:
        books = json.load(my_file)

    pages = list(chunked(books, BOOKS_PER_PAGE))
    total_pages = len(pages)

    env = Environment(loader=FileSystemLoader('.'), autoescape=True)
    template = env.get_template('template.html')

    os.makedirs('docs', exist_ok=True)

    for page_num, books_chunk in enumerate(pages, start=1):
        output_filename = f'index{page_num}.html'
        output_path = os.path.join('docs', output_filename)

        html_output = template.render(
            books=books_chunk,
            page_num=page_num,
            total_pages=total_pages
        )

        with open(output_path, 'w', encoding='utf-8') as my_file:
            my_file.write(html_output)
