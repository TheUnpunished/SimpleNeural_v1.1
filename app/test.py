import time
from selenium import webdriver

#Through cycle go to all of years and do screenshots
#Then open prediction, scroll it and do a screenshot
#Then do a screenshot of project devs
#Done

driver = webdriver.Chrome()
driver.get("localhost:5000")
for x in range(2007, 2018):
    time.sleep(0.8)
    driver.find_element_by_xpath("//select[@name='Select']/option[text()="+str(x)+"]").click()
    time.sleep(0.2)
    driver.find_element_by_xpath("//input[@value='Продолжить']").click()
    time.sleep(2)
    driver.get_screenshot_as_file("screenshots/attendance_"+str(x)+"-"+str(x+1)+".png")
    driver.find_element_by_xpath("//a[@href='/']").click()
time.sleep(0.5)
driver.find_element_by_xpath("//input[@value='Прогноз']").click()
height=driver.execute_script("return document.body.scrollHeight")
x=0
driver.get_screenshot_as_file("screenshots/prediction_" + str(x) + "px.png")
time.sleep(1)
while x<height:
    if x+600>height:
        x=height
    else:
        x+=600
    driver.execute_script("window.scrollTo(0, " + str(x) + ")")
    driver.get_screenshot_as_file("screenshots/prediction_" + str(x) + "px.png")
    time.sleep(1)
driver.find_element_by_xpath("//a[@href='/about/']").click()
driver.get_screenshot_as_file("screenshots/about.png")
time.sleep(2)
driver.close()

