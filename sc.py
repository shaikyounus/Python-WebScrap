from parsel import Selector
import parameters
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
import lxml
import pprint
import smtplib
from email.message import EmailMessage
from string import Template
from pathlib import Path 

html = Template(Path('index.html').read_text())

email=EmailMessage()
email['from']='YOUNUS'
email['to']='mohammadyounus.sk@vitap.ac.in'
email['subject']='Hey I got the data of Linkedin Profiles of your Search Query'



driver = webdriver.Chrome()
driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
sleep(2)
username=driver.find_element_by_id('username')

username.send_keys(parameters.linkedin_username)

password=driver.find_element_by_id('password')

password.send_keys(parameters.linkedin_password)

log_in_button = driver.find_element_by_xpath('//*[@type="submit"]')
log_in_button.click()

driver.get('https:www.google.com')
search_query = driver.find_element_by_name('q')
search_query.send_keys(parameters.search_query)
search_query.send_keys(Keys.RETURN)
res = requests.get(driver.current_url)
soup = BeautifulSoup(res.text, 'html.parser')
#younus= driver.find_elements_by_class_name('r')
younus= driver.find_elements_by_xpath('//*[@id="rso"]/div/div/div/a')
#abc=driver.find_elements_by_css_selector('a').get_attribute('href')
hn=[]
var1=parameters.search_query
print('Searchquery is :'+var1[25:])
linkedin_urls = [url.get_attribute('href') for url in younus]
hn=[]
for i in linkedin_urls:

    driver.get(i)
    sel = Selector(text=driver.page_source)
    
    name = sel.xpath('normalize-space(//li[@class="inline t-24 t-black t-normal break-words"])').extract_first()
    job_title= sel.xpath('normalize-space(//h2[@class="mt1 t-18 t-black t-normal break-words"])').extract_first()
    Location= sel.xpath('normalize-space(//li[@class="t-16 t-black t-normal inline-block"])').extract_first()
    current_url=driver.current_url
    ##index = linkedin_urls.index(i)
    ##email.set_content('Profile ',index)
    if name:
        name=name.strip()
        
    else:
        name="None"
    if job_title:
        job_title=job_title.strip()
        
    else:
        job_title="None"
    if Location:
        Location=Location.strip()
        
    else:
        Location="None"
    
    print('\n')
    print('Name: ' + name)
    print('Job: ' +job_title)
    print('Location '+Location)
    print('Linkedin: ' +current_url)
    email.set_content(html.substitute({'name':name,'Job':job_title, 'Location':Location,'Linkedinurl':current_url}), 'html')
    with smtplib.SMTP(host='smtp.gmail.com',port=587)as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('shaikyounusshaik@gmail.com','Sk#9160296991')
        smtp.send_message(email)
        
    
print('\n')
print('Program Terminated')
"""
import smtplib
from email.message import EmailMessage


email=EmailMessage()
email['from']='YOUNUS'
email['to']='mohammadyounus.sk@vitap.ac.in'
email['subject']='Hey My first Python Email'

email.set_content('Entra  chala cheyyali inka')

with smtplib.SMTP(host='smtp.gmail.com',port=587)as smtp:
    smtp.ehlo()
    smtp.starttls()
    smtp.login('shaikyounusshaik@gmail.com','Sk#9160296991')
    smtp.send_message(email)
    print('Done')
"""
