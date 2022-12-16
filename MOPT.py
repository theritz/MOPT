# first we import a whole bunch of libraries
from flask import Flask, render_template, request
from astropy.coordinates import SkyCoord, EarthLocation, AltAz
from astropy import units
from astropy.time import Time
from astropy.utils.data import download_file
from astropy.io import fits
# because astropy is not all to bright we disable pylint. Yeah...
# pylint: disable=no-member
import mpld3 as mpld3
import matplotlib.pyplot as plt
import numpy as np
import imageio
import re
from time import sleep

# Have Flask join the party
app = Flask(__name__, static_url_path='/static')

# disable cache on static files because Flask is daft or maybe I am (I'll learn... ^_^)
@app.after_request
def apply_caching(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    return response

# let's start the input template
@app.route('/')
def celestobj():
    return render_template('.celestobj.html')

# ..aaand we're back to some processing
@app.route('/',methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        srch = request.form['name']
        # download the DSS image
        image_file = download_file('http://archive.eso.org/dss/dss/image?ra=&dec=&equinox=J2000&name=%s&x=20&y=20&Sky-Survey=DSS1&mime-type=download-fits&statsmode=WEBFORM' % (srch), cache=True )
        image_data = fits.getdata(image_file)
        imageio.imsave('..//MOPT//static//img//DSS.jpg', image_data)
        # scrape the coordinates
        match = str(SkyCoord.from_name(srch))
        coord = [float(val) for val in re.findall(r"[\d.]+", match)]
    # pass all that good stuff to the output template
    return render_template('MOPTgui.html', obj = srch, coord = coord )

# verbose and auto-restart FTW
if __name__ == "__main__":
    app.run(debug = True)
