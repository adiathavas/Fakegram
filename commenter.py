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
import imghdr
import struct

from requests_toolbelt import MultipartEncoder
from . import config



class Instabot:

  def __init__(self, username, password):
    self.username = username
    self.password = password
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--user-agent=Mozilla/5.0 (Linux; Android 6.0; HTC One M9 Build/MRA58K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36");
    chrome_options.add_argument("--start-maximized")
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






  def like_photo(self, hashtag):
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



  """write comment in text area using lambda function"""
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
          self.driver.execute_script("arguments[0].send_keys('');", element)
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

      try:
          comments_block = self.driver.find_elements_by_class_name('XQXOT')
          comments = [x.find_elements_by_tag_name('span') for x in comments_block]
          print(str(len(comments)) + " number of comments")
          for i in range(len(comments)):
            user_comment = re.sub(r'#.\w*', '', comments[i][0].text)
            print(user_comment)

      except NoSuchElementException:
          return ''
      return user_comment

  """have bot comment on picture"""
  def comment_on_picture(self):
      bot = ChatBot('YouTubeChatBot')
      bot.set_trainer(ListTrainer)
      picture_comment = self.get_comments()
      # user's comment and bot's response
      response = bot.get_response(picture_comment).__str__()
      print("User's Comment", picture_comment)
      print("Bot's Response", response)
      return self.post_comment(response)

  def post_photo(self, link, caption, hashtag):
    driver = self.driver
    driver.find_element_by_xpath('//span[@aria-label="New Post"]').click()

def compatible_aspect_ratio(size):
    min_ratio, max_ratio = 4.0 / 5.0, 90.0 / 47.0
    width, height = size
    ratio = width * 1. / height * 1.
    print("FOUND: w:{} h:{} r:{}".format(width, height, ratio))
    return min_ratio <= ratio <= max_ratio

def get_image_size(fname):
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


    def upload_photo(self, photo, caption=None, upload_id=None, from_video=False, force_resize=False, options={}):
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
                photo = resize_image(photo)
            else:
                return False

        with open(photo, 'rb') as f:
            photo_bytes = f.read()

        data = {
            'upload_id': upload_id,
            '_uuid': self.uuid,
            '_csrftoken': self.token,
            'image_compression': '{"lib_name":"jt","lib_version":"1.3.0","quality":"87"}',
            'photo': ('pending_media_%s.jpg' % upload_id, photo_bytes, 'application/octet-stream', {'Content-Transfer-Encoding': 'binary'})
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


def resize_image(fname):
    from math import ceil
    try:
        from PIL import Image, ExifTags
    except ImportError as e:
        print("ERROR: {}".format(e))
        print("Required module `PIL` not installed\n"
              "Install with `pip install Pillow` and retry")
        return False
    print("Analizing `{}`".format(fname))
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
    new_fname = "{}.CONVERTED.jpg".format(fname)
    print("Saving new image w:{w} h:{h} to `{f}`".format(w=w, h=h, f=new_fname))
    new = Image.new("RGB", img.size, (255, 255, 255))
    new.paste(img, (0, 0, w, h), img)
    new.save(new_fname, quality=95)
    return new_fname













# def main():
bot = Instabot('havasresearch', 'havas-reasearch')
bot.login()
bot.post_photo('link', 'living', '#life')
upload_photo(photo = 'computer_kk3W5-0b6e0.jpg', caption='testing')



x = bot.pictures_on_page('toronto')













# print(x)

# for i in range(3):
#   bot.driver.get(x[i])
#   print(bot.get_comments())

# print ("Now going to like a bunch of photos!!!")

# bot.like_photo('amsterdam')










# for pic in bot.pictures_on_page(hashtag='newyork')[1:5]:
#     com.driver.get(pic)
#     time.sleep(3)
#     print('Posted Comment:', com.comment_on_picture())
#     time.sleep(3)

# bot.like_photo('toronto')
# bot.pictures_on_page('toronto')



# if __name__=='__main__':
#   main()
