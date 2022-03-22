import pandas as pd
import requests
import xmltodict
import numpy as np 
import matplotlib.pyplot as plt 
import seaborn as sns; sns.set() 
import warnings 
warnings.filterwarnings('ignore')
import lightgbm as lgb 
from sklearn import datasets
from sklearn.model_selection import train_test_split 
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score
import pickle
import matplotlib
matplotlib.use('Agg')
from backend.apis.address_to_coordinate import address_to_coordinate

import IPython
def display(*dfs, head=True):
    for df in dfs:
        IPython.display.display(df.head() if head else df)

def proprocessing():
    df = pd.read_csv('./data/row_data.csv')

    df['rent_fee'] = df['rent_fee'].str.rstrip('万円').astype('float16') * 10 * 1000
    df['location'] = df['location'].str.lstrip('所在地\n')

    #間取りをone-hot
    df['plan'] = df['plan'].replace('ワンルーム','1')
    df_plan = pd.DataFrame(
        data={
            'plan_R':df['plan'].str[0],
            'plan_L':df['plan'].str.contains('L') * 1,
            'plan_D':df['plan'].str.contains('D') * 1,
            })

    df['year'] = df['year'].str.replace('新築','0').str.lstrip('築').str.rstrip('年').str.rstrip('年以上')
    df['area'] = df['area'].str[:-2]
    df_tatami = pd.DataFrame(data={'tatami':df['plan_detail'].str.contains('和') * 1})
    df_category = pd.DataFrame(
        data={
            'category_small':df['category'].str.contains('アパート|テラス') * 1,
            'category_big':df['category'].str.contains('マンション') * 1,
            'category_alone':df['category'].str.contains('一戸建て') * 1
            })

    df_structure = pd.DataFrame(data={'structure_wooden':df['structure'].str.contains('木造') * 1,})
    df_features = pd.DataFrame(
        data={
            'not_unit_bus' : df['features'].str.contains('バストイレ別') * 1,
            'free_vanity' : df['features'].str.contains('洗面所独立') * 1,
            })

    df['floor'] = df['floor'].str.rstrip('階建').str.replace('平屋','0').str.replace('階/',' ')
    df['floor'] = df['floor'].str[0:2].replace(' ','')
    df['floor'] = df['floor'].str[0]

    df = pd.concat([df,df_plan,df_tatami,df_category,df_structure],axis=1)
    df = df.drop(['category','plan_detail','structure','plan','features'],axis=1)
    df = df.drop_duplicates()

    #アクセス


    start = df['access'].str.find('歩').to_list()
    end = df['access'].str.find('分').to_list()
    access_list = df['access'].to_list()
    access_time_list = []
    
    for i in range(len(access_list)):
        access_time_list.append(access_list[i][start[i] + 1:end[i]])

    df_access_time = pd.DataFrame(data={'access_time':access_time_list}).replace('','100')

    df = pd.concat([df,df_access_time], axis=1)
    df = df.drop(['access'], axis=1)


        #住所
    list_lon = []
    list_lat = []

    for i in df['location']:
        lon,lat =address_to_coordinate(i)
        list_lon.append(lon)
        list_lat.append(lat)

    
    df_loc = pd.DataFrame({'lon': list_lon, 'lat': list_lat})
    df = pd.concat([df, df_loc], axis=1)
    df = df.drop(['location'], axis=1)
    df = df.dropna()


    df = df.dropna()
    df.to_csv('./data/input.csv',index=False)
    return None

def learn():
    return None

def predict(data):
    return None