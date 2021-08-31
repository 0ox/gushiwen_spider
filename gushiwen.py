import requests
from bs4 import BeautifulSoup
import re


def get_soup(link):
    response = requests.get(link, headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')
    return soup


class Website(object):
    """
    title : dict
    """

    def __init__(self, title):
        self.title = title

    def get_detail_link(self):
        result_url = []
        soup = get_soup(source_link)
        for link in soup.find_all(self.title['a']):
            url = link.get(self.title['url'])
            if url is None:
                continue
            elif '/shiwenv_' in url:
                result_url.append(url)
            else:
                continue

        return result_url

    def get_detail_poet(self, url_list):
        # r_poets = []
        for url_par in url_list:
            soup = get_soup(base_link + url_par)
            poet_title = soup.find(self.title['name']).text
            content = soup.find(class_='contson').text.replace('\n', '')
            poet_content = re.split('。', content)
            # poet = json.dumps({'poet_title': poet_title, 'poet_content': poet_content}, ensure_ascii=False)
            poet = ({'poet_title': poet_title, 'poet_content': poet_content})
            yield poet
        #     r_poets.append(poet)
        # return r_poets


if __name__ == '__main__':
    ua = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1664.3 Safari/537.36'
    headers = {'headers': ua}
    base_link = 'https://so.gushiwen.cn/'
    source_link = 'https://m.gushiwen.cn/gushi/shijing.aspx'
    titles = {
        'a': 'a',
        'url': 'href',
        'name': 'h1',
    }
    # test
    # url_list_test = ['/shiwenv_4c5705b99143.aspx', '/shiwenv_db8add908cdb.aspx']
    website = Website(titles)
    urls = website.get_detail_link()
    po = website.get_detail_poet(urls)
    # test_yield
    f = open('poet.txt', 'a+')
    # write to txt
    while True:
        result = next(po)
        for line in result['poet_content']:
            f.write('\n' + str(line))
