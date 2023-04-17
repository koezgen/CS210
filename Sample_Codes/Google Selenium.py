#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

#Next, we will start a new instance of the Chrome web driver and navigate to the Google home page:

path='C:/Users/suuser/Desktop/chromedriver_win32/chromedriver.exe'
driver = webdriver.Chrome(path)
driver.get("https://www.google.com/")

#Then, we will find the search box element and enter a keyword. For this part, we can use XPATH expressions to obtain the required element on the web page. 
# To find the XPATH, we need to investigate the html content of the webpage by clicking on "Inspect".
# After that, either we can copy and paste XPATH expression of the required element, or we can write our own XPATH expressions by analyzing DOM tree.
#For more information on XPATH: https://www.w3schools.com/xml/xpath_syntax.asp

search_box = driver.find_element(By.XPATH, "/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div/div[2]/input")
search_box.send_keys("python tutorial")
search_box.send_keys(Keys.ENTER)

#After the search results load, we will extract the URLs of the top 3 search results:

search_results = driver.find_elements(By.XPATH,("//div[@class='yuRUbf']/a"))
# print the top three links
for i in range(3):
    print(search_results[i].get_attribute("href"))

driver.quit()

