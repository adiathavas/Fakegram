# pull a bunch of images from unsplash using their API


import os
import sys
from pixabay import Image
import urllib.request
import pprint




def main():

  pp = pprint.PrettyPrinter(indent=4)

  # category = ['travel', 'animals', 'nature', 'fashion']
  category = [ 'food', 'computer', 'sports', 'fashion']
  lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
  # api_key = '13065241-0418ed825f53b0418b9b2810a'
  api_key = '13065996-ad3c04acd5537b6de9dcbea87'

  image = Image(api_key)

  for i in category:
    image_response = image.search(
      q=i + ' '+lookup.get(i),
      lang='es',
      image_type='photo',
      orientation='horizontal',
      category= i,
      safesearch='true')
    pp.pprint(image_response)
    prev_image = image_response['hits'][0]['previewURL']
      # print(i + lookup.get(i))
    # urllib.request.urlretrieve(image_response['hits'][0]['previewURL'], 'testing' + i + '.jpg')

  urllib.request.urlretrieve(prev_image, "00000001.jpg")

      # print(image_response)
      # print(image_response['hits'][0]['previewURL'])




if __name__ == "__main__":
    main()



# api key 13065241-0418ed825f53b0418b9b2810a




