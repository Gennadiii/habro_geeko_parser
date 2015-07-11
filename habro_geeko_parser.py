from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path

direction = os.path.expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser.txt')

driver = webdriver.Firefox()
driver.implicitly_wait(30)
driver.get('http://habrahabr.ru/')
first_habratitle = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']").text
doc = open(direction, 'a')

for j in range(5):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		doc.write(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if j == 4:
		doc.write('\n\n\n\n\n\n')
		break
	driver.find_element_by_id('next_page').click()

driver.get('http://geektimes.ru/')
first_geekotitle = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']").text

for j in range(5):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		doc.write(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if j == 4:
		break
	driver.find_element_by_id('next_page').click()
doc.close()

input()

doc = open(direction, 'w')
doc.write(first_habratitle + '\n' + first_geekotitle + '\n\n\n\n')
doc.close()
driver.close()
exit()
