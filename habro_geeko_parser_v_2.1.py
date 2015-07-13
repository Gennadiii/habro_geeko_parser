from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os.path

direction = os.path.expanduser(r'~\Dropbox\Work\Python\Programms\txt\q.txt')
first_titles_list = []
habra_exception = ['тензорной', 'PHP-Дайджест']
geeko_exception = ['Итана', 'NASA', 'НАСА', 'New Horizons']
first_habratitle = ''
first_geekotitle = ''
habro_output = ''
geeko_output = ''


doc = open(direction, 'r') # Getting articles that I've already seen
line = doc.readline()
while line:
	first_titles_list.append(line[:-1])
	line = doc.readline()

driver = webdriver.Firefox()
driver.implicitly_wait(45)
driver.get('http://habrahabr.ru/')
habra_title = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']")
for letter in habra_title.text:
	try:
		first_habratitle += letter
	except UnicodeEncodeError:
		pass

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		flag = None
		if first_titles_list[0] == title.text:
			flag = 'Stop'
			break
		for exception in habra_exception:
			if exception in title.text:
				flag = 'exception'
				break
		if flag != 'exception':
			title_name = ''
			for letter in title.text:
				try:
					print(letter)
					title_name += letter
				except UnicodeEncodeError:
					pass
			habro_output += (title_name + '\n' + str(title.get_attribute('href')) + '\n\n')

	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()


driver.get('http://geektimes.ru/')
geeko_title = driver.find_element_by_xpath("//h1[@class='title']/a[@class='post_title']")
for letter in geeko_title.text:
	try:
		first_geekotitle += letter
	except UnicodeEncodeError:
		pass

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		flag = None
		if first_titles_list[1] == title.text:
			flag = 'Stop'
			break
		for exception in geeko_exception:
			if exception in title.text:
				flag = 'exception'
				break
		if flag != 'exception':
			title_name = ''
			for letter in title.text:
				try:
					print(letter)
					title_name += letter
				except UnicodeEncodeError:
					pass
			geeko_output += (title_name + '\n' + str(title.get_attribute('href')) + '\n\n')

	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()


doc = open(direction, 'w') # Writing current articles to the file
doc.write(first_habratitle + '\n' + first_geekotitle + '\n')
doc.close()
driver.close()
driver.quit()
print(habro_output)
input()
print('\n\n\n'geeko_output)
