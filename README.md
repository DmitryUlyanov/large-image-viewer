# Large image viewer
This is web-based image viewer with a support of arbitrary large images. The image is first broke down into small patches at multiple scales. It allows to load image by parts, exactly as Google Maps loads only part of the map that you look at, at resolution you have.

<table>
    <tr>
        <td><img src="screenshots/1.png"></td>
        <td><img src="screenshots/2.png"></td>
    </tr>
</table>


# Usage

Install `python3`, `flask`, `gevent`, `numpy` and `opencv-python`. (Or use `pip install -r requirements.txt`)

Start viewer with
```
python viewer.py
```

Then open browser at `http://localhost:5123/`, select an image and wait until it is tiled.


# References
[Kaggle plankton visualization](https://github.com/ebenolson/kaggle-ndsb-visualization)

[Polymaps](http://polymaps.org/ex/)
