from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path

direction = os.path.expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser2.txt')
first_titles_list = []
habra_flag = None
geeko_flag = None

doc = open(direction, 'r') # Getting articles that I've already seen
line = doc.readline()
while line:
	first_titles_list.append(line[:-1])
	line = doc.readline()

driver = webdriver.Firefox()
driver.implicitly_wait(45)
driver.get('http://habrahabr.ru/')
first_habratitle = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']").text

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		if first_titles_list[0] == title.text:
			print('\n\n\n\n\n\n')
			habra_flag = True
			break
		elif 'тензорной' in title.text:
			continue
		else:
			print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if habra_flag:
		break
	driver.find_element_by_id('next_page').click()


driver.get('http://geektimes.ru/')
first_geekotitle = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']").text

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		if first_titles_list[1] == title.text:
			geeko_flag = True
			break
		elif 'Итана' in title.text:
			continue
		else:
			print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if geeko_flag:
		break
	driver.find_element_by_id('next_page').click()


doc = open(direction, 'w') # Writing current articles to the file
doc.write(first_habratitle + '\n' + first_geekotitle + '\n')
doc.close()
driver.close()
driver.quit()
