from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from shutil import copyfile
from time import sleep
from os import system, chdir

parol = 
milo = ''

main_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser.txt')
copy_direction = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_parser_copy.txt')
habra_geeko_news = expanduser(r'~\Dropbox\Work\Python\Programms\txt\habra_geeko_news.txt')
first_titles_list = []
habra_exception = ['IaaS-дайджест', 'из мира фронтенда за последнюю неделю', 'Functional C', 'Подпольный рынок кардеров', 'Windows 10 по 10', 'материалов по Ruby', 'из мира Drupal', 'тензорной', 'Дайджест интересных материалов для мобильного разработчика', \
'из мира Drupal', 'материалов по Ruby', 'PHP-Дайджест', 'для iOS-разработчиков', 'из мира веб-разработки и IT']
geeko_exception = ['космоса за неделю', 'Cassini', 'космодром', 'Модули Laurent', 'Проект «Око»', 'МКС', 'Philae', 'Марс', 'Фотографии космоса', 'Церер', 'Curiosity', 'Итана', 'NASA', 'НАСА', 'New Horizons', 'Роскосмос', 'Зонд Dawn']

def clean_news():
    txt = open(habra_geeko_news, 'w')
    txt.write('')
    txt.close()

habra_count = 0
geeko_count = 0
count_rejected = 0

copyfile(main_direction, copy_direction)
clean_news()

news = open(habra_geeko_news, 'a')
doc = open(main_direction, 'r', encoding="utf8") # Getting articles that I've already seen
line = doc.readline()
while line:
    first_titles_list.append(line[:-1])
    line = doc.readline()
doc.close()

driver = webdriver.Firefox()
# driver = webdriver.Chrome(expanduser(r'~\Dropbox\Work\Python\chromedriver.exe'))
driver.get('http://habrahabr.ru/')
#driver.get('http://habrahabr.ru/page4/')

enter = driver.find_element_by_id("login").click()
mail = driver.find_element_by_xpath("//input[@type='email']").send_keys(milo)
password = driver.find_element_by_xpath("//input[@type='password']").send_keys(parol)
submit = driver.find_element_by_xpath("//button[@type='submit']").click()
driver.implicitly_wait(3000)
feed = driver.find_element_by_xpath("//span[@class='tabs-menu__item-text ' and  contains(.,'По подписке')]").click()

titles = "//*[@class='post__title_link']"
list_of_titles_habr_to_file_elements = driver.find_elements_by_xpath(titles)
list_of_titles_habr_to_file = [title.text for title in list_of_titles_habr_to_file_elements]

for j in range(30):
#for j in range(4):
    list_of_titles = driver.find_elements_by_xpath(titles)

    for title in list_of_titles:
        flag = None
        if title.text in first_titles_list:
            news.write('\n\n\n\n\n\n')
            flag = 'Stop'
            break
        for exception in habra_exception:
            if exception in title.text:
                flag = 'exception'
                count_rejected += 1
                break
        if flag != 'exception':
            try:
                news.write(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
            except Exception:
                news.write(str(title.text.encode('unicode_escape')) + '\n' + str(title.get_attribute('href')) + '\n\n')
            habra_count += 1
    if flag == 'Stop':
        break
    driver.find_element_by_id('next_page').click()


driver.get('http://geektimes.ru/')
#driver.get('http://geektimes.ru/page4/')
sleep(2)

feed = driver.find_element_by_xpath("//span[@class='tabs-menu__item-text ' and  contains(.,'По подписке')]")
feed.click()

list_of_titles_geek_to_file_elements = driver.find_elements_by_xpath(titles)
list_of_titles_geek_to_file = [title.text for title in list_of_titles_geek_to_file_elements]

for j in range(30):
#for j in range(4):
    list_of_titles = driver.find_elements_by_xpath(titles)

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
            try:
                news.write(title.text + '\n' + str(title.get_attribute('href')) + '\n\n')
            except Exception:
                news.write(str(title.text.encode('unicode_escape')) + '\n' + str(title.get_attribute('href')) + '\n\n')
            geeko_count += 1
    if flag == 'Stop':
        break
    driver.find_element_by_id('next_page').click()

doc = open(main_direction, 'w', encoding="utf8") # Writing current articles to the file

for j in range(5):
        doc.write(list_of_titles_habr_to_file[j] + '\n')
        doc.write(list_of_titles_geek_to_file[j] + '\n')
doc.close()

news.write('\n\n\n' + str(habra_count) + ' + ' + str(geeko_count) + ' = ' + str(habra_count + geeko_count) + '\n\n\n')
news.write(str(count_rejected) + ' rejected')

news.close()

driver.close()
driver.quit()

chdir(r'C:\Program Files (x86)\Notepad++')
system(r'notepad++.exe' + ' ' + habra_geeko_news)

exit()
