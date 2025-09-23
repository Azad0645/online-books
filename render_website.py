import os
import json
import argparse
import urllib.parse

from more_itertools import chunked
from jinja2 import Environment, FileSystemLoader
from livereload import Server


BOOKS_PER_PAGE = 20


def render(json_path: str = 'meta_data.json'):
    with open(json_path, encoding='utf-8') as my_file:
        books = json.load(my_file)
        for book in books:
            book['img_src'] = urllib.parse.quote(book['img_src'])
            book['book_path'] = urllib.parse.quote(book['book_path'])

    pages = list(chunked(books, BOOKS_PER_PAGE))
    total_pages = len(pages)

    env = Environment(loader=FileSystemLoader('.'), autoescape=True)
    template = env.get_template('template.html')

    os.makedirs(os.path.join('www', 'pages'), exist_ok=True)

    for page_num, books_chunk in enumerate(pages, start=1):
        output_filename = f'index{page_num}.html'
        output_path = os.path.join('www', 'pages', output_filename)

        html_output = template.render(
            books=books_chunk,
            page_num=page_num,
            total_pages=total_pages
        )

        with open(output_path, 'w', encoding='utf-8') as my_file:
            my_file.write(html_output)

    redirect_html = '<meta http-equiv="refresh" content="0; url=pages/index1.html">'
    with open(os.path.join('www', 'index.html'), 'w', encoding='utf-8') as f:
        f.write(redirect_html)


def serve(json_path: str = 'meta_data.json'):
    render(json_path=json_path)

    server = Server()
    server.watch(json_path, lambda: render(json_path=json_path))
    server.watch('template.html', lambda: render(json_path=json_path))

    server.serve(root='www', open_url_delay=1, default_filename='index.html')


def main():
    parser = argparse.ArgumentParser(description='Generate site and optionally run LiveReload.')
    parser.add_argument('--json', dest='json_path', default='meta_data.json',
                        help='Путь к JSON с данными (по умолчанию meta_data.json)')
    parser.add_argument('--serve', action='store_true',
                        help='Запустить LiveReload сервер после сборки')
    args = parser.parse_args()

    if args.serve:
        serve(json_path=args.json_path)
    else:
        render(json_path=args.json_path)


if __name__ == '__main__':
    main()