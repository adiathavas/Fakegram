from django.contrib import admin

# Register your models here.


def like_photo_2(self, hashtag, count):
    counter = count
    driver = self.driver
    driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/?hl=en")
    time.sleep(2)
    for i in range(1, 3):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    pic_hrefs = []

    # going to each picture link and figuring out how to actually like a certain phtoo
    hrefs = driver.find_elements_by_tag_name('a')
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














    def like_photo_2(self, hashtag, count):
        counter = count
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/?hl=en")
        time.sleep(2)
        for i in range(1, 3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)
        pic_hrefs = []

        # going to each picture link and figuring out how to actually like a certain phtoo
        hrefs = driver.find_elements_by_tag_name('a')
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
        print(str(len(pic_hrefs)) + "this is the size of the picsssss")
        for href in pic_hrefs:
            print(href)
            count = count - 1
            print(count)
            if (count <= 0):
                break
            try:
                bot.driver.get(href)
                print("in the try")
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
                    print("in the except  ")
                    time.sleep(2)
                unique_photos -= 1

            except:
                continue
