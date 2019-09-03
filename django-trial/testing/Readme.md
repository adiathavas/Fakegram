# Fakegram

## Fakegram is an Instagram analytics platfrom/assistant that is designed to help marketers with their user workflow.


To run the main UI, follow the following steps:

1) Make sure you have python 3 or later installed

2) pip install all the dependencies from the requirements.txt file in the main folder

3) git clone https://github.com/adiathavas/Fakegram.git

4) Download chromedriver (selenium driver for google chrome) from selenium and put it in each of the following subdirectory: Fakegram main directory, 
    Fakegram/django-trial/testing, Fakegram/django-trial/testing/polls   


5) cd into the folder Fakegram/django-trial/testing and run python manage.py runserver

6) login as you would like a normal IG 

7) If unsuccessful, try again. If successful, choose the action to commit to (only Posting and Quitting fully work right now)





## Next Steps: 

This project is super exciting and there are a lot of really cool things that one could further explore on 

with the project. Below are a list of things that are already done and things that could be the next steps for the project. 

This could truly become something of great value. 



### Accomplished/finished/foundation: 


1) Fake face generator: Used GANs to create fake people based on Flickr dataset. Look at Stylegan_try.ipynb notebook

2) Basic interactions listed on ui using selenium. Liking, commenting, following has been implemented using Selenium driver: look at and run caption_generator.py as a standalone CLI program 

3) Basic UI as a layout of how the main application will look. Run the Ui using the steps above; a basic version foundation of the product is set. 



### Next Steps/Areas of improvement

1) Integration of frameworks with django. After about the first three four days, it became pretty apparent that django as a framework is not very great at vanilla front-end. In fact, it was quite frustrating to deal with. Hence, I was unable to make the UI as appealing as I would have like dit to be. However, with the right setup, I think there's real value in using something like react for the frontend and integrating it with the django backend. 

2) There is a lot to be done on the analytics side. I had tried to set up a follower/following chart growth metric but was unable to do so. To continue work on this, among olther analytics that we might want to include in  the app, make sure to look into InstaBot and using their follower/following fucntions as an auxillary (a resource I found out about much too late)

3) Recommendation of articles for user engagement: After talking to somebody from the marketing side, it became apparent that the posting functionality/feature was the most promising feature for the team. In additon, something else that was considered a pain-point was user engagement was article recommendation.  This had traditionally been done by somebody in the marketing team who would essentially use their own knowledge to find tech articles from their own sources and then repost them on various social medias. This can be automated easily by using the Reddit API to scrape top-voted tech news article or scrape other good article sites. 

