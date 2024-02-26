import argparse
import os

import numpy as np
import cv2

MIN_SIZE = 15
MAX_SIZE = 22

def to_polymap(img, out_path, tile_size=256):

    if isinstance(img, str):
        img = cv2.imread(img)

    if not os.path.exists(out_path):
        os.makedirs(out_path)

    zoom = 0
    while 1:
        print(f'Writing zoom level {zoom}')
        folder_name = os.path.join(out_path, f'zoom{MAX_SIZE - zoom}/')
        if not os.path.exists(folder_name):
            os.makedirs(os.path.join(out_path, f'zoom{MAX_SIZE - zoom}/'))

        h, w, _ = img.shape
        nx = int(np.ceil(w * 1.0 / tile_size))
        ny = int(np.ceil(h * 1.0 / tile_size))
        print(f"Frames: {nx}x{ny}")
        for i in range(nx):
            print(f"Working on column {i}...", end="\r")
            for j in range(ny):
                oi = np.zeros((tile_size, tile_size, 3), dtype='uint8')
                oi[:, :, :] = 255
                x0 = i * tile_size
                y0 = j * tile_size
                x1 = min((i + 1) * tile_size, w)
                y1 = min((j + 1) * tile_size, h)
                oi[0:y1 - y0, 0:x1 - x0, :] = img[y0:y1, x0:x1, :]

                cv2.imwrite(os.path.join(out_path,
                                         f'zoom{MAX_SIZE-zoom}/{i}-{j}.png'), oi)

        if (nx <= 3 and ny <= 3 and zoom >= 2) or MAX_SIZE-zoom < MIN_SIZE:
            return MAX_SIZE-zoom

        zoom += 1
        img = cv2.resize(img, None, fx=0.5, fy=0.5)



def __main__():

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path")
    parser.add_argument("--out_path")
    parser.add_argument("--tile_size", default=256)
    args = parser.parse_args()
    img = cv2.imread(args.img_path)
    to_polymap(img, args.out_path, args.tile_size)
