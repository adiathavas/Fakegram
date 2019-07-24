# pull a bunch of images from unsplash using their API

import os
import sys
import urllib.request
import logging
from pyunsplash import PyUnsplash
import requests

def main():
  response = input("Hello there! What topic would you like to post on today?")
  api_key = "cd9ad8287959d3408ee5c1db5486114901cc1a7aa0c19c31529030b78204be51"
  api_key_imagga = "acc_33cc8a8aef4eadd"
  api_key_imagga_secret = "c83c11035b8d2c13b88a7f9b0f674b4f"


  py_un = PyUnsplash(api_key=api_key)
  my_cmd = 'open /Users/aditya.sharma/Downloads/gan-image-removebg-preview.png'
  print("Great, firstly here is your user persona")
  os.system(my_cmd)
  print("Here are a bunch of images related to your query:")


  if response == "":
    category = [ 'food', 'computer', 'sports', 'fashion']
    # lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
    print(py_un)
    for i in category:
      if (counter > 2):
        break
      q = 'beautiful ' + i
      print(q)
      photos = py_un.search(type_='photos', query = q)
      counter = 0
      print (photos)
      for photo in photos.entries:
        if (counter > 2):
          break
        # run photo through model and get hashtag and captioning
        full_path = os.getcwd() + '/' + 'images/' +  i + '_' + photo.id + '.jpg'
        print(full_path)
        image_url = photo.link_download
        response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,auth=(api_key_imagga, api_key_imagga_secret))
        print(response_i.json().get("result").get("tags")[0])
        urllib.request.urlretrieve(photo.link_download, full_path)


  else:
  # lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
    photos = py_un.search(type_='photos', query = response)
    counter = 0
    for photo in photos.entries:
      counter +=1
      if (counter > 2):
        break
      print("this is the counter number right now")
      # run photo through model and get hashtag and captioning
      full_path = os.getcwd() + '/' + 'images/' + response + '_' + photo.id + '.jpg'


      print(full_path)
      image_url = photo.link_download
      response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,
                        auth=(api_key_imagga, api_key_imagga_secret))
      print(response_i.json().get("result").get("tags")[0])
      urllib.request.urlretrieve(photo.link_download, full_path)
      my_cmd_1 = 'open %s' %full_path
      os.system(my_cmd_1)


  # api 'tings
  # client_secret = "c8eab14f9a07851496021a521635606ea2c233720fc341b7b76aca0739c48d16"
  # redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

  #authorization code
  # code = "9c218e06dedd4f11ddb108a73f86f8ac9f5cdfcef90b92a521e92d7c1378bd0b"
  # category = ['travel', 'animals', 'nature', 'fashion']




if __name__ == "__main__":
    main()



# api key 13065241-0418ed825f53b0418b9b2810a




