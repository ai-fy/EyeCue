import math
import random
import urllib.request
import numpy as np
from PIL import Image
from stqdm import stqdm
import streamlit as st


def crop_image(img):

  if img.width > img.height:
    new_width = img.height
    new_height = img.height

    start_x = (img.width - img.height) / 2
    start_y = 0

    img = img.crop((
        start_x,
        start_y,
        start_x + new_width,
        start_y + new_height,
    ))
  elif img.height > img.width:
    new_width = img.width
    new_height = img.width

    start_x = 0
    start_y = (img.height - img.width) / 2

    img = img.crop((
        start_x,
        start_y,
        start_x + new_width,
        start_y + new_height,
    ))

  return img


def average_colour(image):

  colour_tuple = [None, None, None]
  for channel in range(3):

    # Get data for one channel at a time
    pixels = image.getdata(band=channel)

    values = []
    for pixel in pixels:
      values.append(pixel)

    colour_tuple[channel] = sum(values) / len(values)

  return tuple(colour_tuple)


@st.cache_data
def urls_to_mosaic(url_list, pat=''):

  pass

  urls_shuf = url_list[:100]  # 100 max
  random.seed(12345)
  random.shuffle(urls_shuf)

  #print(f"this is the url_list{url_list}")

  PIL_cropped = download_urls(urls_shuf, pat)

  # attempt to mosaic
  img_list = []
  width = 100
  height = 100
  rows = int(math.sqrt(len(PIL_cropped)))
  columns = int(math.sqrt(len(PIL_cropped)))

  for item in PIL_cropped:
    img_list.append(item[1])

  columns = int(len(img_list) / rows)

  # print(columns)
  # print(width)
  # print(rows)
  # print(height)

  mosaic = Image.new('RGB', (columns * width, rows * height))

  k = 0
  for j in range(0, rows * height, height):
    for i in range(0, columns * width, width):
      # paste the image at location i,j:
      mosaic.paste(img_list[k], (i, j))
      # Select next image
      k = k + 1
  return np.array(mosaic)


@st.cache_data
def download_urls(url_list, pat=''):
  PIL_concept_images = []
  for i, url in stqdm(enumerate(url_list), desc="Downloading images"):
    try:
      hdr = f"Bearer {pat}"
      req = urllib.request.Request(url, headers={"Authorization": hdr, 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'})
      with urllib.request.urlopen(req) as fd:
        im = Image.open(fd)
      PIL_concept_images.append(im)
    except:
      continue

  # crop
  PIL_cropped = []
  for each in stqdm(PIL_concept_images, desc="Pre-processing images"):
    each = crop_image(each)
    each.thumbnail((100, 100))
    each = each.convert("RGB")
    sort_color = average_colour(each)[1]
    im_list = [sort_color, each]
    PIL_cropped.append(im_list)

  PIL_cropped.sort()

  return PIL_cropped
