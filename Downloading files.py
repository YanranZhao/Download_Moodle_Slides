import requests
from bs4 import BeautifulSoup
import re


headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
}

login_data = {
    'username': 'your username',
    'password': 'your password'
}


with requests.Session() as s:
    url = 'https://your_host/moodle/login/index.php'
    r = s.get(url, headers=headers)
    soup = BeautifulSoup(r.text, 'lxml')
    response = s.post(url, data=login_data, headers=headers)

    #  navigate to download page 
    page = s.get('https://your_host/moodle/course/your_course_path')
    html_soup = BeautifulSoup(page.content, 'html.parser')
    print(html_soup.title)

    # match = re.compile('\.(pdf)')
    
    # download all pdf files, all have <a> tag 
    links = html_soup.find_all('a', href=re.compile("resource"))

    for a in links:
        link = a['href']
        file_name = link.split('=')[-1]

        print("Downloading file:%s" % file_name)
        r = requests.get(link, stream=True)

        with open(file_name, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    print("All files downloaded!")
