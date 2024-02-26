from pathlib import Path
import os

from flask import Flask, request, render_template

import tile_img


app = Flask(__name__, static_url_path='', static_folder='static')

if not os.path.exists("last_image.txt"):
    with open("last_image.txt", "w", encoding="utf8") as file:
        file.write("default")

with open("last_image.txt", "r", encoding="utf8") as file:
    LAST_IMAGE = file.readline().strip()
    if LAST_IMAGE == "":
        LAST_IMAGE = "default"

if not os.path.isdir(f'static/tile_{LAST_IMAGE}'):
    ZOOM = tile_img.MIN_SIZE
else:
    ZOOM = tile_img.MAX_SIZE - len(os.listdir(f'static/tile_{LAST_IMAGE}')) + 1

@app.route('/')
def root():
    return render_template('index.html', POLYMAP_PATH=f'tile_{LAST_IMAGE}',
                           MIN_SIZE=tile_img.MIN_SIZE, MAX_SIZE=tile_img.MAX_SIZE,
                           ZOOM=ZOOM)


@app.route('/', methods=['POST'])
def form():
    global LAST_IMAGE, ZOOM
    path = request.form['image_path']
    LAST_IMAGE = Path(path).stem

    with open("last_image.txt", "w", encoding="utf8") as file:
        file.write(LAST_IMAGE)

    if not os.path.isfile(path):
        return render_template('index.html',
                               POLYMAP_PATH=f'tile_{LAST_IMAGE}',
                               MIN_SIZE=tile_img.MIN_SIZE,
                               MAX_SIZE=tile_img.MAX_SIZE,
                               ZOOM=ZOOM,
                               error='Wrong path',
                               form_text=path)

    # shutil.rmtree(f'static/tile_{last_image}', ignore_errors=True)
    if not os.path.isdir(f'static/tile_{LAST_IMAGE}'):
        ZOOM = tile_img.to_polymap(path, f'static/tile_{LAST_IMAGE}')
    else:
        ZOOM = tile_img.MAX_SIZE - len(os.listdir(f'static/tile_{LAST_IMAGE}')) + 1

    return render_template('index.html', POLYMAP_PATH=f'tile_{LAST_IMAGE}',
                           MIN_SIZE=tile_img.MIN_SIZE, MAX_SIZE=tile_img.MAX_SIZE,
                           ZOOM=ZOOM, form_text=path)


if __name__ == "__main__":

    # app.debug = True
    from gevent.pywsgi import WSGIServer
    http_server = WSGIServer(('localhost', 5123), app)
    print("Server is running, address: http://localhost:5123")
    http_server.serve_forever()
