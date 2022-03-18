import os
from csv import writer
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome import service
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
import config

def scraping():
    options = Options()
    options.add_argument('--headless')

    CHROMEDRIVER=config.CHROMEDRIVER
    chrome_service = service.Service(executable_path=CHROMEDRIVER)
    #一覧ページ操作用ドライバ
    driver = webdriver.Chrome(service=chrome_service,options=options)
    #詳細ページ操作用ドライバ
    driver2 = webdriver.Chrome(service=chrome_service,options=options)

    base_url = 'https://suumo.jp/jj/chintai/ichiran/FR301FC005/?ar=020&bs=040&ta=04&sa=01&sngz=&po1=25&po2=99&pc=100'
    driver.get(base_url)

    n_room = driver.find_element(by=By.CLASS_NAME ,value='paginate_set-hit').text.rstrip('件').replace(',','')
    n_page = round(int(n_room),-3) / 100

    if os.path.isfile('./data/row_data.csv'):
        os.remove('./data/row_data.csv')


    with open('./data/row_data.csv', 'w', newline='') as f: 
        header_list =[
            'rent_fee',
            'location',
            'plan',
            'area',
            'category',
            'year',
            'access',
            'features',
            'plan_detail',
            'structure',
            'floor'
        ]
        writer_object = writer(f)
        writer_object.writerow(header_list)
        f.close()

    for i in range(1):#int(n_page)
        print(i+1)
        for page in driver.find_elements(by=By.CLASS_NAME ,value='property_inner-title'):
            url = page.find_element(by=By.TAG_NAME,value='a').get_attribute('href')
            try:
                print(url)
                driver2.get(url)
                rent_fee = driver2.find_element(by=By.CLASS_NAME ,value='property_view_main-emphasis').text
                manage_fee = driver2.find_element(by=By.CLASS_NAME ,value='property_data-body').text

                location = driver2.find_element(by=By.CSS_SELECTOR ,value='.property_view_detail.property_view_detail--location').text

                property_view_list = driver2.find_element(by=By.CSS_SELECTOR ,value='.property_view_detail.property_view_detail--floor_type').text.split()
                plan = property_view_list[2]
                area = property_view_list[4]
                category = property_view_list[8]
                year = property_view_list[10]

                access = driver2.find_element(by=By.CSS_SELECTOR ,value='.property_view_detail.property_view_detail--train').text
                features = driver2.find_element(by=By.CSS_SELECTOR ,value='.bgc-wht.ol-g').text

                overview = driver2.find_element(by=By.CLASS_NAME ,value='table_gaiyou')
                overview_table = overview.find_elements(by=By.TAG_NAME,value='td')
                plan_detail = overview_table[0].text
                structure = overview_table[1].text
                floor = overview_table[2].text

                detail_list = [
                    rent_fee,   #家賃
                    location,   #住所
                    plan,       #間取り
                    area,       #面積
                    category,   #アパート・マンションなど
                    year,       #築年数
                    access,     #最寄交通機関までの時間
                    features,   #特徴
                    plan_detail,#間取り詳細
                    structure,  #木造・鉄筋など
                    floor      #階数
                ]

                with open('./data/row_data.csv', 'a', newline='') as f:  
                    writer_object = writer(f)
                    writer_object.writerow(detail_list)  
                    f.close()

            except NoSuchElementException:
                print("notfind element.")
            except WebDriverException:
                print("not find exception.")

        next_page = driver.find_element(by=By.LINK_TEXT,value='次へ')
        next_page.click()

    driver.quit()