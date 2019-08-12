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
    driver.find_element_by_class_name('glyphsSpriteNew_post__outline__24__grey_9 u-__7')













# def main():
bot = Instabot('havasresearch', 'havas-reasearch')
bot.login()
x = bot.pictures_on_page('toronto')

print(x)

for i in range(3):
  bot.driver.get(x[i])
  print(bot.get_comments())

print ("Now going to like a bunch of photos!!!")

bot.like_photo('amsterdam')
# for pic in bot.pictures_on_page(hashtag='newyork')[1:5]:
#     com.driver.get(pic)
#     time.sleep(3)
#     print('Posted Comment:', com.comment_on_picture())
#     time.sleep(3)

# bot.like_photo('toronto')
# bot.pictures_on_page('toronto')



# if __name__=='__main__':
#   main()
