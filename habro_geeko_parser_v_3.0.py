from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from os.path import expanduser
from shutil import copyfile
from time import sleep, time, strftime
from os import system, chdir, environ

password = 
email = 

txt_folder = expanduser(r'~\Dropbox\Work\Python\Programms\txt2')
old_news_file = txt_folder + '\habra_geeko_old_news.txt'
news_file = txt_folder + '\habra_geeko_news.txt'
backup_news_file = txt_folder + '\habra_geeko_backup_news.txt'
count_rejected_news = 0
list_of_topic_elements = None
note_pad_dir = r'C:\Program Files (x86)\Notepad++'
note_pad = 'notepad++.exe'
page_count = 1


def log(message):
    time = strftime("%H:%M:%S")
    time_stamp = "[ " + time + " ] - "
    print(time_stamp + message)

def write_old_news():
    clean_file(old_news_file)
    log('Writing old news')
    txt = open(old_news_file, 'a')
    for site in sites:
        for new in site['list_of_old_news']:
            try:
                txt.write(new + '\n')
            except Exception: log("Couldn't write old title to file")
    txt.close()

def backup_news():
    log('Backing up news')
    copyfile(news_file, backup_news_file)

def clean_file(file):
    log('Cleaning file: ' + file)
    txt = open(file, 'w')
    txt.write('')
    txt.close()

def get_old_news():
    log('Getting old news')
    result = []
    old_news = open(old_news_file, 'r') # Getting articles that I've already seen
    line = old_news.readline()
    while line:
        result.append(line[:-1])
        line = old_news.readline()
    old_news.close()
    return result

def write_news_to_file(sites):
    log('Writing news to file')
    habr['news'].append({
            'title': '\n\n\n\n\n\n',
            'link': '-'*20 + 'GEEK TIMES' + '-'*20
        })
    news = open(news_file, 'a')

    for site in sites:
        for new in site['news']:
            try:
                news.write(new['title'] + '\n')
            except Exception:
                news.write(str(new['title'].encode('unicode_escape')) + '\n')

            news.write(new['link'] + '\n\n')
    news.close()

def append_news_to_lists(params):
    log('Starting adding news')
    global count_rejected_news
    for page in range(30): # looking for new news on 30 pages
        titles = get_topic_titles()
        for title in titles:
            flag = None
            if title.text in old_news:
                flag = 'Stop'
                break
            for exception in params['not_interesting_news']:
                if exception in title.text:
                    flag = 'exception'
                    count_rejected_news += 1
                    break
            if flag != 'exception':
                try:
                    log('Appending news: ' + title.text)
                except Exception:
                    log('Appending news: encoded')

                params['news'].append({
                        'title': title.text,
                        'link': str(title.get_attribute('href'))
                    })
                params['list_of_old_news'].append(title.text)
                params['news_count'] += 1
        sleep(1)
        if flag == 'Stop':
            break
        open_next_page()

def enough_new_news(sites):
    for site in sites:
        if len(site['list_of_old_news']) < 5:
            input("There's not much news for " + site['host'])
            return False
    return True

def write_summary():
    log('Finishing')
    habra_count = sites[0]['news_count']
    geeko_count = sites[1]['news_count']
    news = open(news_file, 'w')
    news.write(str(habra_count) + ' + ' + str(geeko_count) + ' = ' + str(habra_count + geeko_count) + '\n\n\n' + str(count_rejected_news) + ' rejected' + '\n\n\n')
    news.close()

def open_news_in_notepad():
    log('News are ready to be read')
    chdir(note_pad_dir)
    system(note_pad + ' ' + news_file)

def open_site(site):
    global page_count
    log('Opening site: ' + site)
    page_count = 1
    browser.get(site)

def go_to_login_screen():
    log('Going to login screen')
    browser.find_element_by_id("login").click()

def login():
    log('Logging in')
    browser.find_element_by_xpath("//input[@type='email']").send_keys(email)
    browser.find_element_by_xpath("//input[@type='password']").send_keys(password)
    browser.find_element_by_xpath("//button[@type='submit']").click()

def navigate_to_news():
    log('Navigating to news')
    browser.find_element_by_xpath("//span[@class='tabs-menu__item-text ' and  contains(.,'По подписке')]").click()

def get_topic_titles():
    titles = browser.find_elements_by_xpath("//*[@class='post__title_link']")
    return [title for title in titles]

def open_next_page():
    global page_count
    page_count += 1
    log('Going to next page ' + str(page_count))
    browser.find_element_by_id('next_page').click()


habr =      {'host': 'http://habrahabr.ru/',
             'not_interesting_news': [],
             'news_count': 0,
             'need_to_login': True,
             'list_of_old_news': [],
             'news': []
             }
geektimes = {'host': 'http://geektimes.ru/',
             'not_interesting_news': [],
             'news_count': 0,
             'need_to_login': False,
             'list_of_old_news': [],
             'news': []
             }
sites = [habr, geektimes]


if __name__ == '__main__':
    try:
        browser = webdriver.Firefox()
        # browser = webdriver.Chrome(expanduser(r'~\Dropbox\Work\Python\chromedriver.exe'))
        browser.implicitly_wait(10)
        old_news = get_old_news()
        for site in sites:
            open_site(site['host'])
            if site['need_to_login']:
                go_to_login_screen()
                login()
            navigate_to_news()
            append_news_to_lists(site)
        if not enough_new_news(sites): exit()
        backup_news()
        write_old_news()
        write_summary()
        write_news_to_file(sites)
        browser.close()
        # browser.quit()
        open_news_in_notepad()
        exit()
    except Exception as err:
        input('\n\n\n\t' + str(err))
