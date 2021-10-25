import pandas as pd
import requests as req
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')  # 내부 창을 띄울 수 없으므로 설정
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

read = pd.read_csv('store_info.csv', index_col='store_id')
df = pd.DataFrame(read)

s_link= list(df['s_link'])

s_link_list=[]
for s in s_link:
    s_link_list.append(str(s))

# s_link = str(df['s_link'])
store_name = df['store_name'].to_list()
base_url = 'https://www.siksinhot.com/P/'

index_role = 0
total_nullist=[] # 결측치 있는 부분 알려줌
store_review_onelist=[] #리뷰 한 행이 될 리스트



# 최종 리뷰 csv가 될 df 생성
total_df = pd.DataFrame(index=range(0,1),columns=["store_id","portal_id", "date","score", "review"])

i = 0
for a in range(len(store_name)):
    url = base_url + s_link_list[i]
    i += 1
    print(url)
    driver = webdriver.Chrome('C:/Users/alti1/PycharmProjects/pythonProject/chromedriver.exe', options=chrome_options)
    driver.get(url)
    body = driver.find_element_by_tag_name("body")

    while True:
        try:
            body.send_keys(Keys.PAGE_DOWN)
            time.sleep(1)
            driver.find_element_by_xpath("//*[@id='siksin_review']/div[3]/a/span").click()

        except:
            break

    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")

    contents = body.select("#siksin_review > div.rList > ul > li > div > div.cnt > div.score_story > p")
    contents = [content.text for content in contents]

    stars = body.select("div.score_story > div > span > strong")
    stars = [star.text for star in stars]

    df1 = pd.DataFrame({"store_id": index_role, "portal_id": 1002, "score": stars, "review": contents})
    total_df = pd.concat([total_df, df1])

    total_df.to_csv("test1.csv", encoding='utf-8')


num = []
reviews = []
score = []

for i in range(len(contents)):
  num.append( i + 1 )
  reviews.append( contents[i])
  score.append( stars[i])

info = {'num':num, 'store_name':store_name, 'review':reviews}
df = pd.DataFrame(info)
df.set_index('num', inplace=True)
print(df.head())

df.to_csv('reviews.csv', encoding='utf-8')















# html = driver.page_source
# result = BeautifulSoup(html, 'html.parser')
# time.sleep(10)
# body = result.find("h3")
# store_name = body.select('div.store_name_score > h3 > react-text')

# store_name = driver.find_element_by_xpath('')
# time.sleep(10)
# print(store_name)
# for ptag in store_name:
#     print(ptag.stirng)
#
# response = req.get(url)
# #
# if response.status_code == 200:
#     html = response.text
#     soup = BeautifulSoup(html, 'html.parser')
#     print(soup)
# #
# else:
#     print(response.status_code)

# url = 'https://www.siksinhot.com/P/254650'
