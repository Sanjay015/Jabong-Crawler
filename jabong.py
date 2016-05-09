"""Jabong Crawler."""
import requests
from bs4 import BeautifulSoup
import json
import re


def crawl_jabong():
    """Jabong Data Scrapper."""
    data_list = []
    count = 0
    regx = re.compile('[\n\r\t]')
    _file = open('jabong_data.json', 'w')
    base_url = "http://www.jabong.com/women/clothing"
    r = requests.get(base_url)
    soup = BeautifulSoup(r.content, "html.parser")
    soup_data = soup.find_all(
        "section", {"class": "row search-product animate-products"})[0]
    total_products = int(soup.find_all(
        "span", {"class": "product-count"})[0].text.upper().replace(
        "PRODUCTS", ""))

    for items in soup_data:
        data_dict = {}
        item = items.contents[0]
        try:
            name = item.find_all("div", {"class": "h4"})[0].text
        except:
            name = ''
        data_dict['name'] = name
        try:
            price = item.find_all(
                "span", {"class": "standard-price"})[0].text
        except:
            price = ''
        data_dict['price'] = price
        try:
            img_url = item.find_all("img")[0].get('data-img-config')
            img_url = json.loads(img_url)
            img_url = img_url.get('base_path', '') + img_url.get('1280', '')
        except:
            img_url = ''
        data_dict['image_url'] = img_url
        try:
            product_info = item.get('data-original-href')
        except:
            product_info = ''
        info_dict = {}
        if product_info:
            product_link = base_url + product_info
            prod_html = requests.get(product_link)
            prod_soup = BeautifulSoup(prod_html.content, "html.parser")
            prod_info = prod_soup.find_all(
                "section", {"class": "prod-info"})[0]
            info = prod_info.find_all('div', {'class': 'detail'})[0].text
            try:
                info = regx.sub(' ', info.encode('utf-8'))
            except:
                pass
            data_dict['description'] = info
            details = prod_info.find_all('ul', {'class': 'prod-main-wrapper'})
            for detail in details:
                for element in detail.find_all('li'):
                    category = element.find('label').text.strip()
                    elem = element.find('span').text.strip()
                    if category != 'Authorization':
                        info_dict[category] = elem

        data_dict['product_info'] = info_dict
        data_list.append(data_dict)
        print len(data_list)
        count = count + 1
        # print 'name : ', name
        # print 'price : ', price
        # print 'description : ', info
        # print 'info : ', info_dict
        if(count == total_products):
            break
    _file.write(json.dumps(data_list))
    _file.close()

crawl_jabong()
print 'done.....'
