from flask import Flask, request, render_template
from tile_img import to_polymap
import shutil
import os.path

app = Flask(__name__, static_url_path='', static_folder='static')


@app.route('/')
def root():
    return render_template('index.html', POLYMAP_PATH='tile')


@app.route('/', methods=['POST'])
def form():
    path = request.form['image_path']
    if not os.path.isfile(path):
        return render_template('index.html',
                               POLYMAP_PATH='tile',
                               error='Wrong path',
                               form_text=path)

    shutil.rmtree('static/tile', ignore_errors=True)
    to_polymap(path, 'static/tile')

    return render_template('index.html', POLYMAP_PATH='tile', form_text=path)


if __name__ == "__main__":

    app.debug = True
    from gevent.wsgi import WSGIServer
    http_server = WSGIServer(('localhost', 5123), app)
    http_server.serve_forever()
