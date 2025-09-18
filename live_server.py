from livereload import Server
import render_website


def build():
    render_website.render()

build()

server = Server()
server.watch('meta_data.json', build)
server.watch('template.html', build)

server.serve(root='docs', open_url_delay=1, default_filename='index1.html')