# all the libraries that I will be using

import urllib.request
from pyunsplash import PyUnsplash
from fastai.vision import *
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
import hashlib
import hmac
import imghdr
import struct
import time
import urllib
from json import JSONDecodeError
# import config
from . import config
from . import devices
# import devices
import logging
import os
import sys
import uuid
import requests
import json
from requests_toolbelt import MultipartEncoder
import instabot
from tqdm import tqdm

# set up and keys and stuff

path_pkl = '/Users/aditya.sharma/Desktop/Fakegram'
api_key = "cd9ad8287959d3408ee5c1db5486114901cc1a7aa0c19c31529030b78204be51"
api_key_imagga = "acc_33cc8a8aef4eadd"
api_key_imagga_secret = "c83c11035b8d2c13b88a7f9b0f674b4f"
learn = load_learner(path_pkl)
py_un = PyUnsplash(api_key=api_key)


# class of Instabot
class Instabot:
  # TODO: Figure out why browser opens upon intiializatio and how to stop it
  def __init__(self, username, password, device=None, base_path=''):
    self.username = username
    self.last_json = None
    self.password = password
    self._usernames = {}  # `username` to `user_id` mapping

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--stzart-maximized");
    chrome_options.add_argument("--disable-infobars")
    self.driver = webdriver.Chrome(options=chrome_options)

    device = device or devices.DEFAULT_DEVICE
    self.device_settings = devices.DEVICES[device]
    self.user_agent = config.USER_AGENT_BASE.format(**self.device_settings)
    self.base_path = base_path

    self.is_logged_in = False
    self.last_response = None
    self.total_requests = 0

    # Setup logging
    self.logger = logging.getLogger('[instabot_{}]'.format(id(self)))

    if not os.path.exists("./config/"):
      os.makedirs("./config/")  # create base_path if not exists

    log_filename = os.path.join(base_path, 'instabot.log')
    fh = logging.FileHandler(filename=log_filename)
    fh.setLevel(logging.INFO)
    fh.setFormatter(logging.Formatter('%(asctime)s %(message)s'))

    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter(
      '%(asctime)s - %(levelname)s - %(message)s'))

    self.logger.addHandler(fh)
    self.logger.addHandler(ch)
    self.logger.setLevel(logging.DEBUG)

    self.last_json = None

  def closeBrowser(self):
    self.driver.close()


  @property
  def cookie_dict(self):
        return self.session.cookies.get_dict()

  @property
  def token(self):
      return self.cookie_dict['csrftoken']

  @property
  def user_id(self):
      return self.cookie_dict['ds_user_id']

  @property
  def rank_token(self):
      return "{}_{}".format(self.user_id, self.uuid)

  @property
  def default_data(self):
      return {
          '_uuid': self.uuid,
          '_uid': self.user_id,
          '_csrftoken': self.token,
      }

  def set_user(self, username, password):
      self.username = username
      self.password = password
      self.uuid = self.generate_UUID(uuid_type=True)

  @staticmethod
  def generate_UUID(uuid_type):
      generated_uuid = str(uuid.uuid4())
      if uuid_type:
          return generated_uuid
      else:
          return generated_uuid.replace('-', '')
  @staticmethod
  def generate_device_id(seed):
      volatile_seed = "12345"
      m = hashlib.md5()
      m.update(seed.encode('utf-8') + volatile_seed.encode('utf-8'))
      return 'android-' + m.hexdigest()[:16]

  @staticmethod
  def generate_signature(data):
      body = hmac.new(config.IG_SIG_KEY.encode('utf-8'), data.encode('utf-8'),
                      hashlib.sha256).hexdigest() + '.' + urllib.parse.quote(data)
      signature = 'ig_sig_key_version={sig_key}&signed_body={body}'
      return signature.format(sig_key=config.SIG_KEY_VERSION, body=body)
  @staticmethod
  def get_seed(*args):
      m = hashlib.md5()
      m.update(b''.join([arg.encode('utf-8') for arg in args]))
      return m.hexdigest()


  def save_failed_login(self):
      self.logger.info('Username or password is incorrect.')

  def send_request(self, endpoint, post=None, login=False, with_signature=True, headers=None):
    if (not self.is_logged_in and not login):
      msg = "Not logged in!"
      self.logger.critical(msg)
      raise Exception(msg)

    self.session.headers.update(config.REQUEST_HEADERS)
    self.session.headers.update({'User-Agent': self.user_agent})
    if headers:
      self.session.headers.update(headers)
    try:
      self.total_requests += 1
      if post is not None:  # POST
        if with_signature:
          # Only `send_direct_item` doesn't need a signature
          post = self.generate_signature(post)
        response = self.session.post(
          config.API_URL + endpoint, data=post)
      else:  # GET
        response = self.session.get(
          config.API_URL + endpoint)
    except Exception as e:
      self.logger.warning(str(e))
      return False

    if response.status_code == 200:
      self.last_response = response
      try:
        self.last_json = json.loads(response.text)
        return True
      except JSONDecodeError:
        return False
    else:
      if response.status_code != 404 and response.status_code != "404":
        self.logger.error("Request returns {} error!".format(response.status_code))
      try:
        response_data = json.loads(response.text)
        if "feedback_required" in str(response_data.get('message')):
          self.logger.error("ATTENTION!: `feedback_required`" + str(response_data.get('feedback_message')))
          return "feedback_required"
      except ValueError:
        self.logger.error("Error checking for `feedback_required`, response text is not JSON")

      if response.status_code == 429:
        sleep_minutes = 5
        self.logger.warning(
          "That means 'too many requests'. I'll go to sleep "
          "for {} minutes.".format(sleep_minutes))
        time.sleep(sleep_minutes * 60)
      elif response.status_code == 400:
        response_data = json.loads(response.text)

        # PERFORM Interactive Two-Factor Authentication
        if response_data.get('two_factor_required'):
          self.logger.info("Two-factor authentication required")
          two_factor_code = input("Enter 2FA verification code: ")
          two_factor_id = response_data['two_factor_info']['two_factor_identifier']

          login = self.session.post(config.API_URL + 'accounts/two_factor_login/',
                                    data={'username': self.username,
                                          'verification_code': two_factor_code,
                                          'two_factor_identifier': two_factor_id,
                                          'password': self.password,
                                          'device_id': self.device_id,
                                          'ig_sig_key_version': 4
                                          },
                                    allow_redirects=True)

          if login.status_code == 200:
            resp_json = json.loads(login.text)
            if resp_json['status'] != 'ok':
              if 'message' in resp_json:
                self.logger.error("Login error: {}".format(resp_json['message']))
              else:
                self.logger.error(
                  "Login error: \"{}\" status and message {}.".format(resp_json['status'],
                                                                      login.text))
              return False
            return True
          else:
            self.logger.error("Two-factor authentication request returns {} error with message {} !".format(
              login.status_code, login.text))
            return False
        # End of Interactive Two-Factor Authentication
        else:
          msg = "Instagram's error message: {}"
          self.logger.info(msg.format(response_data.get('message')))
          if 'error_type' in response_data:
            msg = 'Error type: {}'.format(response_data['error_type'])
          self.logger.info(msg)

      # For debugging
      try:
        self.last_response = response
        self.last_json = json.loads(response.text)
      except Exception as e:
        pass
      return False

  def set_proxy(self):
    if self.proxy:
      parsed = urllib.parse.urlparse(
        self.proxy)  # figyuure out what's wrongfigyuure out what's wrongfigyuure out what's wrongfigyuure out what's wrongfigyuure out what's wrong
      scheme = 'http://' if not parsed.scheme else ''
      self.session.proxies['http'] = scheme + self.proxy
      self.session.proxies['https'] = scheme + self.proxy

  def load_cookie(self, fname):

    try:
      with open(fname, 'r') as f:
        self.session = requests.Session()
        self.session.cookies = requests.utils.cookiejar_from_dict(json.load(f))
      cookie_username = self.cookie_dict['ds_user']
      assert cookie_username == self.username
    except FileNotFoundError:
      raise Exception('Cookie file `{}` not found'.format(fname))
    except (TypeError, EOFError):
      os.remove(fname)
      msg = ('An error occured opening the cookie `{}`, '
             'it will be removed an recreated.')
      raise Exception(msg.format(fname))
    except AssertionError:
      msg = 'The loaded cookie was for {} instead of {}.'
      raise Exception(msg.format(self.username))

  def save_cookie(self, fname):
    with open(fname, 'w') as f:
      json.dump(requests.utils.dict_from_cookiejar(self.session.cookies), f)

  def save_successful_login(self, use_cookie, cookie_fname):
    self.is_logged_in = True
    self.logger.info("Logged-in successfully as '{}'!".format(self.username))
    print(devices.DEFAULT_DEVICE)
    if use_cookie:
      self.save_cookie(cookie_fname)
      self.logger.info("Saved cookie!")

  def solve_challenge(self):
    challenge_url = self.last_json['challenge']['api_path'][1:]
    try:
      self.send_request(challenge_url, None, login=True, with_signature=False)
    except Exception as e:
      self.logger.error(e)
      return False
    choices = self.get_challenge_choices()
    for choice in choices:
      print(choice)
    code = input('Insert choice: ')

    data = json.dumps({'choice': code})
    try:
      self.send_request(challenge_url, data, login=True)
    except Exception as e:
      self.logger.error(e)
      return False

    print('A code has been sent to the method selected, please check.')
    code = input('Insert code: ')

    data = json.dumps({'security_code': code})
    try:
      self.send_request(challenge_url, data, login=True)
    except Exception as e:
      self.logger.error(e)
      return False
    worked = (('logged_in_user' in self.last_json) and (self.last_json.get('action', '') == 'close') and (
              self.last_json.get('status', '') == 'ok'))
    if worked:
      return True
    self.logger.error('Not possible to log in. Reset and try again')
    return False

  def get_challenge_choices(self):
    last_json = self.last_json
    choices = []

    if last_json.get('step_name', '') == 'select_verify_method':
      choices.append("Checkpoint challenge received")
      if 'phone_number' in last_json['step_data']:
        choices.append('0 - Phone')
      if 'email' in last_json['step_data']:
        choices.append('1 - Email')

    if last_json.get('step_name', '') == 'delta_login_review':
      choices.append("Login attempt challenge received")
      choices.append('0 - It was me')
      choices.append('0 - It wasn\'t me')

    if not choices:
      choices.append(
        '"{}" challenge received'.format(
          last_json.get('step_name', 'Unknown')))
      choices.append('0 - Default')

    return choices

  def login_browser (self):
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



  def login(self, force=False, proxy=None,
            use_cookie=False, cookie_fname=None):

    username, password = 'portia_res', 'havas-reasearch'
    # idk if i need this or not
    self.device_id = self.generate_device_id(self.get_seed(username, password))

    # again, not sure if needed
    self.proxy = proxy

    self.set_user(username, password)

    if not cookie_fname:
      cookie_fname = "{username}_cookie.txt".format(username=username)
      cookie_fname = os.path.join(self.base_path, cookie_fname)

    cookie_is_loaded = False
    if use_cookie:
      try:
        self.load_cookie(cookie_fname)
        cookie_is_loaded = True
        self.is_logged_in = True
        self.set_proxy()  # Only happens if `self.proxy`
        self.logger.info("Logged-in successfully as '{}' using the cookie!".format(self.username))
        return True
      except Exception:
        print("The cookie is not found, but don't worry `instabot`"
              " will create it for you using your login details.")

    if not cookie_is_loaded and (not self.is_logged_in or force):
      self.session = requests.Session()
      self.set_proxy()  # Only happens if `self.proxy`
      url = 'si/fetch_headers/?challenge_type=signup&guid={uuid}'
      url = url.format(uuid=self.generate_UUID(False))
      if self.send_request(url, login=True):
        data = json.dumps({
          'phone_id': self.generate_UUID(True),
          '_csrftoken': self.token,
          'username': self.username,
          'guid': self.uuid,
          'device_id': self.device_id,
          'password': self.password,
          'login_attempt_count': '0',
        })

        if self.send_request('accounts/login/', data, True):
          self.save_successful_login(use_cookie, cookie_fname)
          return True
        elif self.last_json.get('error_type', '') == 'checkpoint_challenge_required':
          self.logger.info('Checkpoint challenge required...')
          solved = self.solve_challenge()
          if solved:
            self.save_successful_login(use_cookie, cookie_fname)
            print('yay!')

            return True
          else:
            self.save_failed_login()
            print(' no yay!')

            return False
        else:
          self.save_failed_login()
          return False



  def json_data(self, data=None):
    """Adds the default_data to data and dumps it to a json."""
    if data is None:
      data = {}
    data.update(self.default_data)
    return json.dumps(data)

  def configure_photo(self, upload_id, photo, caption=''):
    (w, h) = get_image_size(photo)
    data = self.json_data({
      'media_folder': 'Instagram',
      'source_type': 4,
      'caption': caption,
      'upload_id': upload_id,
      'device': self.device_settings,
      'edits': {
        'crop_original_size': [w * 1.0, h * 1.0],
        'crop_center': [0.0, 0.0],
        'crop_zoom': 1.0
      },
      'extra': {
        'source_width': w,
        'source_height': h,
      }})
    return self.send_request('media/configure/?', data)

  def expose(self):
    data = self.json_data({
      'id': self.user_id,
      'experiment': 'ig_android_profile_contextual_feed'
    })
    return self.send_request('qe/expose/', data)

  def upload_photo(self, photo, caption=None, upload_id=None, from_video=False, force_resize=True, options={}):
    """Upload photo to Instagram

    @param photo         Path to photo file (String)
    @param caption       Media description (String)
    @param upload_id     Unique upload_id (String). When None, then generate automatically
    @param from_video    A flag that signals whether the photo is loaded from the video or by itself (Boolean, DEPRECATED: not used)
    @param force_resize  Force photo resize (Boolean)
    @param options       Object with difference options, e.g. configure_timeout, rename (Dict)
                         Designed to reduce the number of function arguments!
                         This is the simplest request object.

    @return Boolean
    """
    options = dict({
      'configure_timeout': 15,
      'rename': True
    }, **(options or {}))
    if upload_id is None:
      upload_id = str(int(time.time() * 1000))
    if not photo:
      return False
    if not compatible_aspect_ratio(get_image_size(photo)):
      self.logger.error('Photo does not have a compatible photo aspect ratio.')
      if force_resize:
        print('currecntly resizing!!')
        photo = resize_image(photo)
      else:
        print('resizing failed!!!!')

        return False

    with open(photo, 'rb') as f:
      photo_bytes = f.read()

    data = {
      'upload_id': upload_id,
      '_uuid': self.uuid,
      '_csrftoken': self.token,
      'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
      'photo': ('pending_media_%s.jpg' % upload_id, photo_bytes, 'application/octet-stream',
                {'Content-Transfer-Encoding': 'binary'})
    }
    m = MultipartEncoder(data, boundary=self.uuid)
    self.session.headers.update({'X-IG-Capabilities': '3Q4=',
                                 'X-IG-Connection-Type': 'WIFI',
                                 'Cookie2': '$Version=1',
                                 'Accept-Language': 'en-US',
                                 'Accept-Encoding': 'gzip, deflate',
                                 'Content-type': m.content_type,
                                 'Connection': 'close',
                                 'User-Agent': self.user_agent})
    response = self.session.post(
      config.API_URL + "upload/photo/", data=m.to_string())

    configure_timeout = options.get('configure_timeout')
    if response.status_code == 200:
      for attempt in range(4):
        if configure_timeout:
          time.sleep(configure_timeout)
        if self.configure_photo(upload_id, photo, caption):
          media = self.last_json.get('media')
          self.expose()
          if options.get('rename'):
            from os import rename
            rename(photo, "{}.REMOVE_ME".format(photo))
          return media
    return False


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

  def actions(self):
    print("These are the things that you can do with this application."
          " These include \n\tPosting photos \n\tGetting analytics "
          "\n\tCommenting on your own content \n\tLiking other people's posts"
          " \n\tCommenting on other people's posts "
          "\n\tFollowing other people \n\tQuit")

    response_2 = input("Type the first letter of the command that you would like to do today! \n")
    if response_2 == 'P':
        self.post()
    if response_2 == 'G':
        # TODO
        resp = input("What type of analytics would you like to collect? "
                     "\n\tOwn analytics (type Own) \n\tOther's analytics (type Others) \n")
        if resp == "Own":
            print("Great, let's get started!")
            self.own_analytics()
        if resp == "Others":
            resp1 = input("Great, let's get started - type the username of the IG that you want to get analytics on")
            self.others_analytics(resp1)

    if response_2 == 'L':
        response = input("Great! What hashtag would you like to post pictures of?")
        print("Liking a bunch of photos with the hashtag! Just close up the browser once you are done!")
        self.like_photo(response)
    if response_2 == 'C':
      # TODO
        self.post_comment('Hello!')
    if response_2 == 'F':

        self.post()
    if response_2 == 'Y':
      # TODO
        self.post()
    if response_2 == "" or response_2 == "Q":
        print("Thanks for stopping by - have a good day!")
        sys.exit()

  def own_analytics(self):
    print('Here are some statistics about your account: ')
    print('Number of Followers: ' + self.get_user_followers(self.username))
    print('blha')

  def get_user_followers(self, user_id, nfollows = None ):
    user_id = self.convert_to_user_id(user_id)
    followers = self.get_total_followers(user_id, nfollows)
    return [str(item['pk']) for item in followers][::-1] if followers else []

  def others_analytics(self, other_usrname):
    print('asd')

  def get_total_followers(self, user_id, amount=None):
      return self.get_total_followers_or_followings(
          user_id, amount, 'followers')

  def get_username_info(self, user_id):
    url = 'users/{user_id}/info/'.format(user_id=user_id)
    return self.send_request(url)


  def get_user_followings(self, user_id, max_id=''):
      url = 'friendships/{user_id}/following/?max_id={max_id}&ig_sig_key_version={sig_key}&rank_token={rank_token}'
      url = url.format(
          user_id=user_id,
          max_id=max_id,
          sig_key=config.SIG_KEY_VERSION,
          rank_token=self.rank_token
      )
      return self.send_request(url)

  def get_total_followers_or_followings(self,
                                        user_id,
                                        amount=None,
                                        which='followers',
                                        filter_private=False,
                                        filter_business=False,
                                        filter_verified=False,
                                        usernames=False,
                                        to_file=None,
                                        overwrite=False):
      from io import StringIO

      if which == 'followers':
          key = 'follower_count'
          get = self.get_user_followers
      elif which == 'followings':
          key = 'following_count'
          get = self.get_user_followings

      sleep_track = 0
      result = []
      next_max_id = ''
      self.get_username_info(user_id)
      username_info = self.last_json
      if "user" in username_info:
          total = amount or username_info["user"][key]

          if total > 200000:
              print("Consider temporarily saving the result of this big "
                    "operation. This will take a while.\n")
      else:
          return False
      if filter_business:
          print("--> You are going to filter business accounts. This will take time! <--")
      if to_file is not None:
          if os.path.isfile(to_file):
              if not overwrite:
                  print("File `{}` already exists. Not overwriting.".format(to_file))
                  return False
              else:
                  print("Overwriting file `{}`".format(to_file))
          with open(to_file, 'w'):
              pass
      desc = "Getting {} of {}".format(which, user_id)
      with tqdm(total=total, desc=desc, leave=True) as pbar:
          while True:
              get(user_id, next_max_id)
              last_json = self.last_json
              try:
                  with open(to_file, 'a') if to_file is not None else StringIO() as f:
                      for item in last_json["users"]:
                          if filter_private and item['is_private']:
                              continue
                          if filter_business:
                              time.sleep(2 * random.random())
                              self.get_username_info(item['pk'])
                              item_info = self.last_json
                              if item_info['user']['is_business']:
                                  continue
                          if filter_verified and item['is_verified']:
                              continue
                          if to_file is not None:
                              if usernames:
                                  f.write("{}\n".format(item['username']))
                              else:
                                  f.write("{}\n".format(item['pk']))
                          result.append(item)
                          pbar.update(1)
                          sleep_track += 1
                          if sleep_track >= 20000:
                              sleep_time = random.uniform(120, 180)
                              msg = "\nWaiting {:.2f} min. due to too many requests."
                              print(msg.format(sleep_time / 60))
                              time.sleep(sleep_time)
                              sleep_track = 0
                  if not last_json["users"] or len(result) >= total:
                      return result[:total]
              except Exception as e:
                  print("ERROR: {}".format(e))
                  return result[:total]

              if last_json["big_list"] is False:
                  return result[:total]

              next_max_id = last_json.get("next_max_id", "")

  def convert_to_user_id(self, x):
    x = str(x)
    if not x.isdigit():
      x = x.lstrip('@')
      x = self.get_user_id_from_username(x)
    # if type is not str than it is int so user_id passed
    return x

  def get_user_id_from_username(self, username):
    if username not in self._usernames:
      self.search_username(username)
      self.very_small_delay()
      if "user" in self.last_json:
        self._usernames[username] = str(self.last_json["user"]["pk"])
      else:
        return None
    return self._usernames[username]

  def very_small_delay(self):
      time.sleep(random.uniform(0.175, 0.875))

  def search_username(self, username):
    url = 'users/{username}/usernameinfo/'.format(username=username)
    return self.send_request(url)

  def post_2(self, argument):

      photos = py_un.search(type_='photos', query=argument)
      divisor = 1
      collection = []
      small_collection =[]
      for photo in photos.entries:
          if divisor % 5 == 0:   # if there are 5 phtoos in a collection already
            small_collection.append(photo)
            collection.append(small_collection)
            small_collection = []
            collection
            divisor = 1
          small_collection.append(photo)
          divisor += 1






      for photo in photos.entries:
          # run photo through model and get hashtag and captioning

          image_url = photo.link_download
          full_path = os.getcwd() + '/' + 'images/' + '_' + photo.id + '.jpg'
          urllib.request.urlretrieve(photo.link_download, full_path)

          # TODO: make own model
          response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,
                                    auth=(api_key_imagga, api_key_imagga_secret))
          tags = []
          time.sleep(1)
          for i in range(5):
              tags.append(response_i.json().get("result").get("tags")[i].get("tag").get("en"))

          # TODO: Figure out how to increase classification and generate comments based on classification using AI
          answer = classify(full_path, learn)
          caption = caption_generate(answer, tags)
          self.upload_photo(full_path, caption)
          break


  #open up  'open /Users/aditya.sharma/Downloads/gan-image-removebg-preview.png'


  def post(self, argument=None):

    if argument == None:
        # getting what user wants to post on
        response = [str(x) for x in input("What topic would you like to post on today? \n").split()]
        response = ''.join(response)

        # printing user profile picture ;
        print("Great, firstly here is your user persona")
        # TODO: dynamic creation
        my_cmd = 'open /Users/aditya.sharma/Downloads/gan-image-removebg-preview.png'
        os.system(my_cmd)

        # actually fetching the image from unsplash for you
        if response == "":

            print("Oops! Looks like you didn't input any query - picking a random category for you!\n")
            response = random_category()
            print("Your category will be " + response)

        photos = py_un.search(type_='photos', query=response)
        print("\n Now that we have that out of the way, here are a bunch of images related to your query:")
        counter = 0

        for photo in photos.entries:

            # finding photo user likes and wants to post

            print(photo.link_download)
            self.driver.get(photo.link_download)
            time.sleep(3)
            answer = input('Do you like this photo? \n')

            if answer == 'yes':
                # run photo through model and get hashtag and captioning

                full_path = os.getcwd() + '/' + 'images/' + response + '_' + photo.id + '.jpg'
                image_url = photo.link_download
                urllib.request.urlretrieve(photo.link_download, full_path)

                # TODO: make own model
                response_i = requests.get('https://api.imagga.com/v2/tags?image_url=%s' % image_url,
                                          auth=(api_key_imagga, api_key_imagga_secret))
                tags = []
                print("Great, we really like that picture too! These are some of the tags you could use for captioning \n")
                for i in range(5):
                    tags.append(response_i.json().get("result").get("tags")[i].get("tag").get("en"))
                    print('#' + tags[i] + '\n')

                # TODO: Figure out how to increase classification and generate comments based on classification using AI
                answer = classify(full_path, learn)
                caption = caption_generate(answer, tags)
                self.upload_photo(full_path, caption)
                break
            else:
                print("No Problem, let's try another photo!")
                continue
    else:
        pass





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

  # TODO: have a lot more of these comments
  print( "And therefore a comment could be:\n\n" + class_dict.get(str(pred_class) ))
  list_return = [pred_class, class_dict.get(str(pred_class) ) ]
  return list_return




def get_image_size(fname='image.jpg'):
  with open(fname, 'rb') as fhandle:
    head = fhandle.read(24)
    if len(head) != 24:
      raise RuntimeError("Invalid Header")

    if imghdr.what(fname) == 'png':
      check = struct.unpack('>i', head[4:8])[0]
      if check != 0x0d0a1a0a:
        raise RuntimeError("PNG: Invalid check")
      width, height = struct.unpack('>ii', head[16:24])
    elif imghdr.what(fname) == 'gif':
      width, height = struct.unpack('<HH', head[6:10])
    elif imghdr.what(fname) == 'jpeg':
      fhandle.seek(0)  # Read 0xff next
      size = 2
      ftype = 0
      while not 0xc0 <= ftype <= 0xcf:
        fhandle.seek(size, 1)
        byte = fhandle.read(1)
        while ord(byte) == 0xff:
          byte = fhandle.read(1)
        ftype = ord(byte)
        size = struct.unpack('>H', fhandle.read(2))[0] - 2
      # We are at a SOFn block
      fhandle.seek(1, 1)  # Skip `precision' byte.
      height, width = struct.unpack('>HH', fhandle.read(4))
    else:
      raise RuntimeError("Unsupported format")
    return width, height



def resize_image(fname):
  from math import ceil
  try:
    from PIL import Image, ExifTags
    print('trying!!')
  except ImportError as e:
    print("ERROR: {}".format(e))
    print("Required module `PIL` not installed\n"
          "Install with `pip install Pillow` and retry")
    return False

  print("Analyzing `{}`".format(fname))
  h_lim = {'w': 90., 'h': 47.}
  v_lim = {'w': 4., 'h': 5.}
  img = Image.open(fname)
  (w, h) = img.size
  deg = 0
  try:
    for orientation in ExifTags.TAGS.keys():
      if ExifTags.TAGS[orientation] == 'Orientation':
        break
    exif = dict(img._getexif().items())
    o = exif[orientation]
    if o == 3:
      deg = 180
    if o == 6:
      deg = 270
    if o == 8:
      deg = 90
    if deg != 0:
      print("Rotating by {d} degrees".format(d=deg))
      img = img.rotate(deg, expand=True)
      (w, h) = img.size
  except (AttributeError, KeyError, IndexError) as e:
    print("No exif info found (ERR: {})".format(e))
    pass
  img = img.convert("RGBA")
  ratio = w * 1. / h * 1.
  print("FOUND w:{w}, h:{h}, ratio={r}".format(w=w, h=h, r=ratio))
  if w > h:
    print("Horizontal image")
    if ratio > (h_lim['w'] / h_lim['h']):
      print("Cropping image")
      cut = int(ceil((w - h * h_lim['w'] / h_lim['h']) / 2))
      left = cut
      right = w - cut
      top = 0
      bottom = h
      img = img.crop((left, top, right, bottom))
      (w, h) = img.size
    if w > 1080:
      print("Resizing image")
      nw = 1080
      nh = int(ceil(1080. * h / w))
      img = img.resize((nw, nh), Image.ANTIALIAS)
  elif w < h:
    print("Vertical image")
    if ratio < (v_lim['w'] / v_lim['h']):
      print("Cropping image")
      cut = int(ceil((h - w * v_lim['h'] / v_lim['w']) / 2))
      left = 0
      right = w
      top = cut
      bottom = h - cut
      img = img.crop((left, top, right, bottom))
      (w, h) = img.size
    if h > 1080:
      print("Resizing image")
      nw = int(ceil(1080. * w / h))
      nh = 1080
      img = img.resize((nw, nh), Image.ANTIALIAS)
  else:
    print("Square image")
    if w > 1080:
      print("Resizing image")
      img = img.resize((1080, 1080), Image.ANTIALIAS)
  (w, h) = img.size
  new_fname = "{}".format(fname)
  print("this is the new filename!!!!!!" + new_fname)
  print("Saving new image w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
  new = Image.new("RGB", img.size, (255, 255, 255))
  new.paste(img, (0, 0, w, h), img)
  new.save(new_fname, quality=95)
  return new_fname

def compatible_aspect_ratio(size):
  min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
  width, height = size
  ratio = width * 1. / height * 1.
  print("FOUND: w:{} h:{} r:{}".format(width, height, ratio))
  return min_ratio <= ratio <= max_ratio

def caption_generate(classifier, tags):

  caption = str(classifier[1])

  for i in range(len(tags)):
    caption = caption + ' #' + str(tags[i])
  return caption


def random_category():

    #TODO: make this list larger
    category = ['food', 'computer', 'sports', 'fashion']

    import numpy as np
    return category[np.random.randint(low = 0, high = len(category) -1)]


def main():

    bot = Instabot('portia_res', 'havas-reasearch')
    bot.login()
    print("Hello there!")
    bot.actions()


if __name__ == "__main__":
    main()
