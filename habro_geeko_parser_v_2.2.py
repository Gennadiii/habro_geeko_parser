from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from shutil import copyfile
from time import sleep

parol = ''
milo = ''

main_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser.txt')
copy_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser_copy.txt')
first_titles_list = []
habra_exception = ['Windows 10 по 10', 'материалов по Ruby', 'из мира Drupal', 'тензорной', 'Дайджест интересных материалов для мобильного разработчика', \
'из мира Drupal', 'материалов по Ruby', 'PHP-Дайджест', 'для iOS-разработчиков', 'из мира веб-разработки и IT']
geeko_exception = ['Curiosity', 'Итана', 'NASA', 'НАСА', 'New Horizons', 'Роскосмос', 'Зонд Dawn']

habra_count = 0
geeko_count = 0
count_rejected = 0

copyfile(main_direction, copy_direction)

doc = open(main_direction, 'r', encoding="utf8") # Getting articles that I've already seen
line = doc.readline()
while line:
    first_titles_list.append(line[:-1])
    line = doc.readline()
doc.close()

driver = webdriver.Firefox()
driver.implicitly_wait(45)
driver.get('http://habrahabr.ru/')
#driver.get('http://habrahabr.ru/page4/')

enter = driver.find_element_by_xpath("//span[@class='g-icon g-icon-lock']")
enter.click()
mail = driver.find_element_by_xpath("//input[@type='email']")
mail.send_keys(milo)
password = driver.find_element_by_xpath("//input[@type='password']")
password.send_keys(parol)
submit = driver.find_element_by_xpath("//button[@type='submit']")
submit.click()
feed = driver.find_element_by_xpath("//span[@class='name' and  contains(.,'По подписке')]")
feed.click()

list_of_titles_habr_to_file = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

for j in range(20):
#for j in range(4):
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
		        count_rejected += 1
		        break
		if flag != 'exception':
			print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
			habra_count += 1
	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()


driver.get('http://geektimes.ru/')
#driver.get('http://geektimes.ru/page4/')
sleep(2)

feed = driver.find_element_by_xpath("//span[@class='name' and  contains(.,'По подписке')]")
feed.click()

list_of_titles_geek_to_file = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

for j in range(20):
#for j in range(4):
	list_of_titles = driver.find_elements_by_xpath("//h1[@class='title']/a[@class='post_title']")

	for title in list_of_titles:
		flag = None
		if title.text in first_titles_list:
		    flag = 'Stop'
		    break
		for exception in geeko_exception:
		    if exception in title.text:
		        flag = 'exception'
		        count_rejected += 1
		        break
		if flag != 'exception':
		    print(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
		    geeko_count += 1
	if flag == 'Stop':
		break
	driver.find_element_by_id('next_page').click()

doc = open(main_direction, 'w', encoding="utf8") # Writing current articles to the file

for j in range(5):
        doc.write(list_of_titles_habr_to_file[j].text + '\n')
        doc.write(list_of_titles_geek_to_file[j].text + '\n')
doc.close()

print('\n\n\n' + str(habra_count) + ' + ' + str(geeko_count) + ' = ' + str(habra_count + geeko_count) + '\n\n\n')
print(str(count_rejected) + ' rejected')

driver.close()
driver.quit()
