# pull a bunch of images from unsplash using their API

import os
import sys
import urllib.request
import logging
from pyunsplash import PyUnsplash

def main():

  # api 'tings
  api_key = "cd9ad8287959d3408ee5c1db5486114901cc1a7aa0c19c31529030b78204be51"
  # client_secret = "c8eab14f9a07851496021a521635606ea2c233720fc341b7b76aca0739c48d16"
  # redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

  #authorization code
  # code = "9c218e06dedd4f11ddb108a73f86f8ac9f5cdfcef90b92a521e92d7c1378bd0b"
  py_un = PyUnsplash(api_key=api_key)
  # category = ['travel', 'animals', 'nature', 'fashion']

  category = [ 'food', 'computer', 'sports', 'fashion']
  # lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
  print(py_un)
  for i in category:
    q = 'beautiful ' + i
    print(q)

    photos = py_un.search(type_='photos', query = q)

    print (photos)
    for photo in photos.entries:
      full_path = os.getcwd() + '/' + i + '_' + photo.id + '.jpg'
      print(full_path)
      urllib.request.urlretrieve(photo.link_download, full_path)



if __name__ == "__main__":
    main()



# api key 13065241-0418ed825f53b0418b9b2810a




