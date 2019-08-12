# pull a bunch of images from unsplash using their API

import os
import sys
import urllib.request
import logging
from pyunsplash import PyUnsplash
import requests
from fastai.vision import *
import time
import random
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import pickle



class Instabot:

  def __init__(self, username, password):
    self.username = username
    self.password = password



    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36");
    chrome_options.add_argument("--start-maximized");
    chrome_options.add_argument("--disable-infobars")
    self.driver = webdriver.Chrome(options=chrome_options)
    self.driver.set_window_size(750,900)
    # firefox_capabilities = webdriver.DesiredCapabilities.FIREFOX
    # firefox_capabilities['marionette'] = True
    # PROXY = "58.216.202.149:8118"
    # firefox_capabilities['proxy'] = {
    # "proxyType": "MANUAL",
    # "httpProxy": PROXY,
    # "ftpProxy": PROXY,
    # "sslProxy": PROXY
    # }
    # self.driver = webdriver.Firefox(capabilities=firefox_capabilities)
    # self.driver = webdriver.Firefox()





  def closeBrowser(self):
    self.driver.close()





  def login(self):
    driver = self.driver
    driver.get("https://www.instagram.com/accounts/login/?hl=en")
    time.sleep(3)
    user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
    user_name_elem.clear()
    user_name_elem.send_keys(self.username)

    password_elem = driver.find_element_by_xpath("//input[@name='password']")
    password_elem.clear()
    password_elem.send_keys(self.password)
    password_elem.send_keys(Keys.RETURN)
    # popup = driver.find_element_by_xpath("//button[@class='aOOlW HoLwm']")
    ui.WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".aOOlW.HoLwm"))).click()
    time.sleep(2)


  def post_photo(self, link, caption, hashtag):
    driver = self.driver
    driver.find_element_by_class_name('glyphsSpriteNew_post__outline__24__grey_9 u-__7')



  def like_photo(self, hashtag, count):
    counter = count
    driver = self.driver
    driver.get("https://www.instagram.com/explore/tags/"+hashtag+"/?hl=en")
    time.sleep(2)
    for i in range(1,3):
      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
      time.sleep(2)
    pic_hrefs =[]

    #going to each picture link and figuring out how to actually like a certain phtoo
    hrefs= driver.find_elements_by_tag_name('a')
    # pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
    # pic_hrefs = [href for href in pic_hrefs if hashtag in href]
    # print(hashtag + ' photos: ' + str(len(hrefs)))
    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs]
    # building list of unique photos
    for href in hrefs_in_view:
      if href not in pic_hrefs:
        pic_hrefs.append(href)
    # for href in hrefs:

    #   try:
    #     driver.get(href)
    #   except:
    #     print("skipping this bro" + href)
    #     continue
    #   driver.execute_script("window.scrollTo(0. document.body.scrollHeight);")
    #   try:
    #     driver.find_element_by_link_text("Like").click()
    #     time.sleep(20)
    #   except:
    #     time.sleep(2)
    #   print("SUCEEESS!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    for href in pic_hrefs:
      count = count - 1
      if (count <= 0):
        break
      try:
        bot.driver.get(href)
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            time.sleep(random.randint(2, 4))
            like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
            like_button().click()
            for second in reversed(range(0, random.randint(18, 28))):
                print("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                + " | Sleeping " + str(second))
                time.sleep(1)
        except Exception as e:
            time.sleep(2)
        unique_photos -= 1

      except:
        continue





  def pictures_on_page(self, hashtag):
    driver = self.driver
    driver.get("https://www.instagram.com/explore/tags/"+hashtag+"/?hl=en")
    time.sleep(2)
    pic_hrefs = []

    for i in range(1,3):
      try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        hrefs= driver.find_elements_by_tag_name('a')
        hrefs_in_view = [elem.get_attribute('href') for elem in hrefs]
        # building list of unique photos
        for href in hrefs_in_view:
          if href not in pic_hrefs:
            pic_hrefs.append(href)
        # print("Check: pic href length " + str(len(pic_hrefs)))

      except Exception:
        continue
    return pic_hrefs


    #going to each picture link and figuring out how to actually like a certain phtoo
    # pic_hrefs = [elem.get_attribute('href') for elem in hrefs]
    # pic_hrefs = [href for href in pic_hrefs if hashtag in href]
    # print(hashtag + ' photos: ' + str(len(hrefs)))


      # try:
      #   driver.get(href)
      # except:
      #   print("skipping this bro" + href)
      #   continue
      # driver.execute_script("window.scrollTo(0. document.body.scrollHeight);")
      # try:
      #   driver.find_element_by_link_text("Like").click()
      #   time.sleep(20)
      # except:
      #   time.sleep(2)
      # print("SUCEEESS!!!!!!!!!!!!!!!!!!!!!!!!!!!!")



  """write comment in text area using lamcbda function"""
  def write_comment(self, comment_text):
      try:
          comment_button = lambda: self.driver.find_element_by_link_text('Comment')
          comment_button().click()
      except NoSuchElementException:
          pass

      try:
          time.sleep(3)
          comment_box_elem = lambda: self.driver.find_element_by_xpath("//textarea[@aria-label='Add a comment…']")
          element = WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.XPATH, "//textarea[@aria-label='Add a comment…']")))
          self.driver.execute_script("arguments[0].click();", element)
          # comment_box_elem().send_keys('')
          comment_box_elem().clear()
          for letter in comment_text:
              comment_box_elem().send_keys(letter)
              time.sleep((random.randint(1, 7) / 30))

          return comment_box_elem

      except StaleElementReferenceException and NoSuchElementException as e:
          print(e)
          return False


  """actually post a comment"""
  def post_comment(self, comment_text):
      time.sleep(random.randint(1,5))

      comment_box_elem = self.write_comment(comment_text)
      if comment_text in self.driver.page_source:
          comment_box_elem().send_keys(Keys.ENTER)
          try:
              post_button = lambda: self.driver.find_element_by_xpath("//button[@type='Post']")
              post_button().click()
              print('clicked post button')
          except NoSuchElementException:
              pass

      time.sleep(random.randint(4, 6))
      self.driver.refresh()
      if comment_text in self.driver.page_source:
          return True
      return False


  """grab comments from a picture page"""
  def get_comments(self):
      # load more comments if button exists
      time.sleep(3)
      user_comment = ''
      try:
          comments_block = self.driver.find_elements_by_class_name('XQXOT')
          comments = [x.find_element_by_tag_name('span') for x in comments_block]

          print(comments)

          try:
            user_comment = re.sub(r'#.\w*', '', comments[0].text)
            print(user_comment)
          except Exception:
            pass

      except NoSuchElementException:
          return ''
      return user_comment



  """have bot comment on picture"""
  def comment_on_picture(self):
      bot = ChatBot('IGbot')
      trainer = ListTrainer(bot)
      picture_comment = self.get_comments()
      # user's comment and bot's response
      f = open('./InstagramComments_.p', 'rb')
      comments = pickle.load(f)
      f.close()

      #Training Bot with existing comments
      for convo in comments[:500]:
          trainer.train(convo)

      response = bot.get_response(picture_comment).__str__()
      print("User's Comment", picture_comment)
      print("Bot's Response", response)
      return self.post_comment(response)




def classify(img_path, learner):
  learn = learner
  class_dict = {'beaches': 'A day for the memory book',
  'nature': 'What a beautiful view!',
  'icecream': 'Cheat days are to be cherished!!',
  'food': 'Best meal I have ever had!!',
  'computer': 'This beauty is a keeper!',
  'sports': 'Action action action!',
  'fashion': 'You know how we roll'}
  classes = ['beaches', 'nature', 'icecream', 'food', 'computer', 'sports', 'fashion']
  img = open_image(img_path)
  pred_class,pred_idx,outputs = learn.predict(img)

  print("Our model detects that this is a photo of")
  print(pred_class)
  print( "And therefore a comment could be:\n\n" + class_dict.get(str(pred_class) ))
  list_return = [pred_class, class_dict.get(str(pred_class) ) ]
  return list_return


def post():
  response = [ str(x) for x in input("Hello there! What topic would you like to post on today? \n").split()]
  api_key = "cd9ad8287959d3408ee5c1db5486114901cc1a7aa0c19c31529030b78204be51"
  api_key_imagga = "acc_33cc8a8aef4eadd"
  api_key_imagga_secret = "c83c11035b8d2c13b88a7f9b0f674b4f"


  response = ''.join(response)
  py_un = PyUnsplash(api_key=api_key)
  print("Great, firstly here is your user persona")

  my_cmd = 'open /Users/aditya.sharma/Downloads/gan-image-removebg-preview.png'
  os.system(my_cmd)


  print("Now that we have that out of the way, here are a bunch of images related to your query:")


  if response == "":
    counter = 0

    print("Looks like you didn't input any query - here are some of our favourite photos!")
    category = ['food', 'computer', 'sports', 'fashion']
    for i in category:
      counter +=1

      if (counter > 2):
        break
      q = 'beautiful ' + i

      counter_1 = 0
      photos = py_un.search(type_='photos', query = q)
      for photo in photos.entries:
        if (counter_1 > 2):
          break
        counter_1 += 1
        # run photo through model and get hashtag and captioning
        full_path = os.getcwd() + '/' + 'images/' +  i + '_' + photo.id + '.jpg'

        image_url = photo.link_download
        response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,auth=(api_key_imagga, api_key_imagga_secret))
        # print(response_i.json().get("result").get("tags")[0])
        urllib.request.urlretrieve(photo.link_download, full_path)

        tags = []
        tags.append(response_i.json().get("result").get("tags")[0].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[1].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[2].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[3].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[4].get("tag").get("en"))

        print(tags)

        classify(full_path, learn)
        my_cmd_1 = 'open %s' %full_path
        os.system(my_cmd_1)



  else:
  # lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
    photos = py_un.search(type_='photos', query = response)
    counter = 0
    for photo in photos.entries:
      counter +=1
      if (counter > 2):
        break
      # run photo through model and get hashtag and captioning
      full_path = os.getcwd() + '/' + 'images/' + response + '_' + photo.id + '.jpg'
      image_url = photo.link_download
      urllib.request.urlretrieve(photo.link_download, full_path)

      response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url, auth=(api_key_imagga, api_key_imagga_secret))
      tags = []
      tags.append(response_i.json().get("result").get("tags")[0].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[1].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[2].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[3].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[4].get("tag").get("en"))

      print(tags)

      classify(full_path, learn)

      my_cmd_1 = 'open %s' %full_path
      os.system(my_cmd_1)



def main():
  print("yo")
  path_pkl = '/Users/aditya.sharma/Desktop/Fakegram'
  learn = load_learner(path_pkl)
  classes = ['beaches', 'nature', 'icecream', 'food', 'computer', 'sports', 'fashion']

  class_dict = {'beaches': 'A day for the memory book',
    'nature': 'What a beautiful view!',
    'icecream': 'Cheat days are to be cherished!!',
    'food': 'Best meal I have ever had!!',
    'computer': 'This beauty is a keeper!',
    'sports': 'Action action action!',
    'fashion': 'You know how we roll'}


  response = [ str(x) for x in input("Hello there! What topic would you like to post on today? \n").split()]
  api_key = "cd9ad8287959d3408ee5c1db5486114901cc1a7aa0c19c31529030b78204be51"
  api_key_imagga = "acc_33cc8a8aef4eadd"
  api_key_imagga_secret = "c83c11035b8d2c13b88a7f9b0f674b4f"


  response = ''.join(response)
  py_un = PyUnsplash(api_key=api_key)
  print("Great, firstly here is your user persona")

  my_cmd = 'open /Users/aditya.sharma/Downloads/gan-image-removebg-preview.png'
  os.system(my_cmd)


  print("Now that we have that out of the way, here are a bunch of images related to your query:")


  if response == "":
    counter = 0

    print("Looks like you didn't input any query - here are some of our favourite photos!")
    category = ['food', 'computer', 'sports', 'fashion']
    for i in category:
      counter +=1

      if (counter > 2):
        break
      q = 'beautiful ' + i

      counter_1 = 0
      photos = py_un.search(type_='photos', query = q)
      for photo in photos.entries:
        if (counter_1 > 2):
          break
        counter_1 += 1
        # run photo through model and get hashtag and captioning
        full_path = os.getcwd() + '/' + 'images/' +  i + '_' + photo.id + '.jpg'

        image_url = photo.link_download
        response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,auth=(api_key_imagga, api_key_imagga_secret))
        # print(response_i.json().get("result").get("tags")[0])
        urllib.request.urlretrieve(photo.link_download, full_path)

        tags = []
        tags.append(response_i.json().get("result").get("tags")[0].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[1].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[2].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[3].get("tag").get("en"))
        tags.append(response_i.json().get("result").get("tags")[4].get("tag").get("en"))
        for i in tags:
          i = '#' + i
        print("These are a list of hashtags that you could use to describe your image!")
        print(tags)

        classify(full_path, learn)
        my_cmd_1 = 'open %s' %full_path
        os.system(my_cmd_1)



  else:
  # lookup = {'food': 'nice', 'computer': 'cool', 'sports': 'fun', 'fashion': 'trendy'}
    photos = py_un.search(type_='photos', query = response)
    counter = 0
    for photo in photos.entries:
      counter +=1
      if (counter > 2):
        break
      # run photo through model and get hashtag and captioning
      full_path = os.getcwd() + '/' + 'images/' + response + '_' + photo.id + '.jpg'
      image_url = photo.link_download
      urllib.request.urlretrieve(photo.link_download, full_path)

      response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url, auth=(api_key_imagga, api_key_imagga_secret))
      tags = []
      tags.append(response_i.json().get("result").get("tags")[0].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[1].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[2].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[3].get("tag").get("en"))
      tags.append(response_i.json().get("result").get("tags")[4].get("tag").get("en"))
      for i in tags:
        i = '#' + i
      print("These are a list of hashtags that you could use to describe your image!")
      print(tags)


      answer = classify(full_path, learn)

      bot = Instabot('havasresearch', 'havas-reasearch')
      bot.login()

      my_cmd_1 = 'open %s' %full_path
      os.system(my_cmd_1)

  print("There are a bunch of other things that you can do with this application. These include \n\tPosting the photos generated \n\tGetting analytics \n\tCommenting on your own content \n\tLiking other people's posts \n\tCommenting on other people's posts \n\tFollowing other people \n\tQuit")
  response_2 = input("Type the first letter of the command that you would like to do! \n")
  switch_python = {
    'P':'Post',
    'G':'Get',
    'L':'Like',
    'C':'Comment_own',
    'F':'Follow',
    'Y':'Comment_others',
    'Q':'Quit session'
  }

  if (response_2 == "" or response_2 == "Q"):
    resp_3 = print("Thanks for stopping by - have a good day!")
    sys.exit()

  elif(response_2 == "G"):
    print("You currently have no data - keep IG'ing!")

  elif response_2 == "L" :
    resp_l = input("Great, what tag do you want to like on?")
    resp_count = input("As well, how many?")

    print("Here we go!")
    bot = Instabot('havasresearch', 'havas-reasearch')
    bot.login()
    bot.like_photo(resp_l, resp_count)



  elif response_2 == "C" :
    bot = Instabot('havasresearch', 'havas-reasearch')
    bot.login()
    response = input("What tag do you want to comment on?")
    resp_chatbot = bot.pictures_on_page(response)

    print("Here is a potential comment you can post!!")
    for i in range(3):
      bot.driver.get(resp_chatbot[i])
      print("Firstly, here are some comments posted on the image " + bot.get_comments() )
      bot.comment_on_picture()
      time.sleep(2)
    print("have a great day!")



  elif response_2 == "F" :
    bot = Instabot('havasresearch', 'havas-reasearch')
    bot.login()
    print("This feature is currently under development; try again later. Have a great day!")


  elif response_2 == "Y" :
    bot = Instabot('havasresearch', 'havas-reasearch')
    bot.login()
    print("have a great day!")


  elif response_2 == "P" :
    print("Yikes! Instagram currently doesn't support posting images through the web portal - try using the ones we created on your phone!")






  # api 'tings
  # client_secret = "c8eab14f9a07851496021a521635606ea2c233720fc341b7b76aca0739c48d16"
  # redirect_uri = "urn:ietf:wg:oauth:2.0:oob"

  #authorization code
  # code = "9c218e06dedd4f11ddb108a73f86f8ac9f5cdfcef90b92a521e92d7c1378bd0b"
  # category = ['travel', 'animals', 'nature', 'fashion']




if __name__ == "__main__":
    main()
