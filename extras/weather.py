import xbmc
import os
import re
import requests
import shutil
import time

settings_path = xbmcvfs.translatePath('special://home/userdata/addon_data/skin.auramod/settings.xml')
image_store_path = os.path.join(os.path.dirname(__file__), 'weather/weather-%s.gif' % time.strftime("%Y%m%d-%H%M%S"))
image_store_dir = os.path.dirname(image_store_path)

shutil.rmtree(image_store_dir, ignore_errors=True)
os.makedirs(image_store_dir)

with open(settings_path) as settings:
    settings_content = settings.read()

url = re.findall(r'<setting id="weather_image_url" type="string">(.*?)<\/setting>', settings_content)
if len(url) > 0:
    url = url[0]
else:
    # fallback to default image
    url = 'http://sirocco.accuweather.com/nx_mosaic_640x480_public/sir/inmasirFL_.gif'

image_response = requests.get(url, stream=True)
if image_response.status_code == 200:
    with open(image_store_path, 'wb') as image_file:
        image_response.raw.decode_content = True
        shutil.copyfileobj(image_response.raw, image_file)
