# stackoverflowscraper
A simple stack overflow scraper to find questions based on keyword search

For example, to get the stackoverflow questions about **android** posted past week, type the below command:
```
python2.7 scraper.py --searchfor=android
```
similary, for php:

```
python2.7 scraper.py --searchfor=php
```
The top 10 questions in terms of created date and most voted will be listed along with additional details

![output table](https://raw.githubusercontent.com/shimul-iut/stackoverflowscraper/master/image1.JPG)

# viewing the individual question thread:

After the lists are displayed, the console will invoke for the ID of the question you would like to see the full thread. After entering the ID, the console will open the browser view of the correpsonding URL inside the console

![terminal invoke](https://raw.githubusercontent.com/shimul-iut/stackoverflowscraper/master/image2.JPG)

# python version
2.7
