import argparse
import os
import numpy as np
import skimage.transform
import skimage.io
import scipy.misc


def to_polymap(img, out_path, tile_size=256):

    if isinstance(img, str) or isinstance(img, unicode):
        img = skimage.io.imread(img)

    if not os.path.exists(out_path):
        os.makedirs(out_path)
    img = skimage.img_as_ubyte(img)
    zoom = 0
    while 1:
        print 'Writing zoom level {0}'.format(zoom)
        folder_name = os.path.join(out_path, 'zoom%d/' % (20 - zoom))
        if not os.path.exists(folder_name):
            os.makedirs(os.path.join(out_path, 'zoom%d/' % (20 - zoom)))

        h, w, _ = img.shape
        nx = int(np.ceil(w * 1.0 / tile_size))
        ny = int(np.ceil(h * 1.0 / tile_size))
        for i in range(nx):
            for j in range(ny):
                oi = np.zeros((tile_size, tile_size, 3), dtype='uint8')
                oi[:, :, :] = 255
                x0 = i * tile_size
                y0 = j * tile_size
                x1 = min((i + 1) * tile_size, w)
                y1 = min((j + 1) * tile_size, h)
                oi[0:y1 - y0, 0:x1 - x0, :] = img[y0:y1, x0:x1, :]

                scipy.misc.imsave(os.path.join(out_path, 'zoom%d/' %
                                               (20 - zoom)) + '/%d-%d.png' % (i, j), oi)

        if nx <= 3 and ny <= 3 and zoom >= 2:
            break

        zoom += 1
        img = skimage.img_as_ubyte(skimage.transform.rescale(img, (.5, .5)))


def __main__():

    parser = argparse.ArgumentParser()
    parser.add_argument("--img_path")
    parser.add_argument("--out_path")
    parser.add_argument("--tile_size", default=256)
    args = parser.parse_args()
    img = skimage.io.imread(args.img_path)
    to_polymap(img, args.out_path, args.tile_size)
