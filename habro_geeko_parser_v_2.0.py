from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from shutil import copyfile

main_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser.txt')
copy_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser_copy.txt')
first_titles_list = []
habra_exception = ['материалов по Ruby', 'из мира Drupal', 'тензорной', 'Дайджест интересных материалов для мобильного разработчика', \
'из мира Drupal', 'материалов по Ruby', 'PHP-Дайджест', 'для iOS-разработчиков', 'из мира веб-разработки и IT']
geeko_exception = ['Итана', 'NASA', 'НАСА', 'New Horizons']

copyfile(main_direction, copy_direction)

doc = open(main_direction, 'r') # Getting articles that I've already seen
line = doc.readline()
while line:
    first_titles_list.append(line[:-1])
    line = doc.readline()
doc.close()

driver = webdriver.Firefox()
driver.implicitly_wait(45)
driver.get('http://habrahabr.ru/')

list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

doc = open(main_direction, 'w') # Writing current articles to the file
for j in range(5):
        doc.write(list_of_titles[j].text + '\n')

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		flag = None
		if title.text in first_titles_list:
		    print('\n\n\n\n\n\n')
		    flag = 'Stop'
		    break
		for exception in habra_exception:
		    if exception in title.text:
		        flag = 'exception'
		        break
		if flag != 'exception':
			print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()


driver.get('http://geektimes.ru/')

list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

for j in range(5):
        doc.write(list_of_titles[j].text + '\n')
doc.close()

for j in range(20):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		flag = None
		if title.text in first_titles_list:
		    flag = 'Stop'
		    break
		for exception in geeko_exception:
		    if exception in title.text:
		        flag = 'exception'
		        break
		if flag != 'exception':
		    print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()

driver.close()
driver.quit()
