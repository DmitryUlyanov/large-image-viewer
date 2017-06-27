var po = org.polymaps;

var map = po.map()
    .container(document.getElementById("map").appendChild(po.svg("svg")))
    .zoomRange([15, 20])
    .zoom(15)
    .add(po.image().url('POLYMAP_PATH/zoom{Z}/{X}-{Y}.png'))
    .add(po.interact())
    .add(po.compass().pan("none"))
    .center({lat: 85.051, lon: -179.975});