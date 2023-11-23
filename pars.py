import requests
import re
import pandas as pd
from bs4 import BeautifulSoup

def find_article(str_element):
    str_article = str_element
    str_article = re.findall('data-sku="\d+"', str_article)
    str_article = re.findall('\d+', str(str_article))
    # print(int(str_article[0]))
    return(int(str_article[0]))

def find_by_URL(URL):
    response = requests.get(URL)
    html_content = response.content
    soup = BeautifulSoup(html_content, "html.parser")
    return soup

# url = "https://online.metro-cc.ru/category/bakaleya"# metro
url = "https://online.metro-cc.ru/category/tovary-dlya-doma-dachi-sada"

soup = find_by_URL(url)

df_products = pd.DataFrame(columns=["id товара","наименование","ссылка на товар","регулярная цена","бренд"])

products = soup.find_all(class_="catalog-1-level-product-card product-card with-rating with-prices-drop")

for card in products:

    #Ссылка на товар
    url_adr = "https://online.metro-cc.ru" + card.find("a")["href"]

    # Цена товара
    price = card.find(class_="product-price__sum-rubles").text.strip()

    #Переход на карточку товара
    card_page = find_by_URL(url_adr)

    # Название товара
    card_page_title = card_page.find('h1').text.strip()

    # Бренд
    li_block = card_page.find(class_="product-attributes__list-item-link reset-link active-blue-text")

    # "id товара","наименование","ссылка на товар","регулярная цена","бренд"
    #сборка df.row
    append_list = []
    # Артикул
    append_list.append(find_article(str(card)))
    # Название товара
    append_list.append(card_page_title)
    # Ссылка на товар
    append_list.append(url_adr)
    # Цена
    append_list.append(price)
    #Бренд
    append_list.append(li_block.text.strip())
    df_products.loc[len(df_products)] = append_list

    # print("Название товара:", card_page_title)
    # print("Ссылка на товар:", url_adr)
    # print("Цена товара:", price)
    # print("Артикль товара:", find_article(str(card)))
    # print("Бренд:", li_block.text.strip())

df_products.to_csv('result.csv',index=False)



