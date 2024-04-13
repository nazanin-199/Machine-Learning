import re 
import requests
from bs4 import BeautifulSoup
import mysql.connector
from unidecode import unidecode
from datetime import date 



database = mysql.connector.connect(user='admin', host='localhost', database='DigikalaPhones1', password='password')
cursor=database.cursor()
print('connected to DataBase ')
# connected to MariaDB

main_url='https://www.digikala.com/search/category-mobile-phone/?sortby=4'
page=requests.get(main_url)
soup= BeautifulSoup(page.content, 'html.parser')
page_num=soup.find(class_='c-pager__items')
last_page=re.findall(r'data-page=\"(\d+)\"', str(page_num.find(class_='c-pager__next')))
####
# I have not enough internet so i wont use exact last page so i put the pages 5 
print('Connected to main page')
total_page=1
for i in range(1, total_page+1):
    new_url=('https://www.digikala.com/search/category-mobile-phone/?pageno=%d&sortby=4'%i)
    new_page=requests.get(new_url)
    soup1=BeautifulSoup(new_page.content, 'html.parser')
    
    phones= soup1.find(class_='c-listing__items')
    items=phones.find_all(class_='c-product-box__content')
    phones_model=[re.sub(r'[A-Za-z/0-9-]+ \w+ [[sS]+[iI]+[mM+].*$','',item.find(class_='c-product-box__title-en').get_text()).split() for item in items]
    price=[]
    for item in items :    
        if item.find(class_='c-price__value-wrapper')==None:
            pri=item.find(class_='c-promotion-box__cover-text js-product-status').get_text()
        else:
            pri=unidecode(item.find(class_='c-price__value-wrapper').get_text().rsplit(' ',1)[0].strip())
        price.append(pri)
    anchors=soup1.find_all('a', {'class':'c-product-box__img c-promotion-box__image js-url js-product-item js-product-url', 'href':True})
    
    os=[]
    internal_memmory=[]
    ram=[]
    os_version=[]
    picture_resolution=[]
    technology=[]
    
    for anchor in anchors:
        string1=anchor['href']
        string='https://www.digikala.com'
        url=string+string1
        p1=requests.get(url)
        s2=BeautifulSoup(p1.content, 'html.parser')
        ex_info=s2.find_all('ul', {'data-title':"ویژگی‌های محصول"})
        group1=[ ex.get_text().split() for ex  in ex_info]
        internal_memmory.append(group1[0][2])
        for i in range(3, len(group1[0])):
            if group1[0][i]=='سیستم':
                os.append(group1[0][i+2])
                break
        ex_info1=s2.find_all('li', {'class':'js-more-attrs c-product__params-more'})
        group2=[ex.get_text().split() for ex in ex_info1] 

        
        for  i in range (0 , len(group2)):
            if 'مقدار RAM' in (' '.join(group2[i])) : 
                ram.append(re.findall(r'\d+',''.join( group2[0])))
            elif 'رزولوشن عکس' in (' '.join(group2[i])):
                picture_resolution.append(re.findall(r'\d+',''.join(group2[1])))
            elif 'نسخه سیستم عامل' in (' '.join(group2[i])):
                os_version.append(re.findall(r'[A-Za-z]* \d+',' '.join(group2[2])))
            elif 'فناوری' in (' '.join(group2[i])):
                technology.append(re.findall(r'[A-Za-z]+',' '.join(group2[3])))
    
#all datas are stored in lists :)

#inserting data in data base 

today=str(date.today()) 
num= len(phones_model)
for i in range(0, len(phones_model)):
    cursor.execute('INSERT INTO phones_info VALUES (\'%s\' ,\'%s\', \'%s\' ,\'%s\', \'%s\', \'%s\', \'%s\', \'%s\', \'%s\')'%(''.join(phones_model[i]) , price[i] ,internal_memmory[i] , ''.join(ram[i]) , os[i] ,''.join(os_version[i]) ,''.join(picture_resolution[i]) , ''.join(technology[i]), today ))
    
    database.commit()

print('datas are stored ')
