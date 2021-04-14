from bs4 import BeautifulSoup
import xlsxwriter
import requests
from selenium import webdriver
import time
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

def conv(s):
    a = s.split('.')
    l = len(a)
    result = 0
    for i in range(0,l):
        result+=int(a[i])*(1000**(l-i-1))
    return result

print("Nhập từ khóa:")
keyword = input()
record = {
    'Tên':[],
    'Giá cũ':[],
    'Giá mới':[],
    'Thương hiệu':[],
    'Danh mục thể loại':[],
    'Link ảnh':[],
    'Link sản phẩm':[]
}

#   
#                                                                    Tiki
df = pd.DataFrame(data=record)



page = 1
row = 1
while page < 11:

    url = 'https://tiki.vn/search?q=' + keyword + '&_lc=Vk4wMzQwMjMwMDg=&page=' + str(page)
    result = requests.get(url)

    print(result.url)
    cont = result.text
    soup = BeautifulSoup(cont ,'html5lib')

    productlisting = soup.find("div", class_="product-listing").find("div", class_="product-box-list")
    products = productlisting.find_all("div",class_="product-item")
    
    for x in products :
        if x == None :
            continue

        regular = x.find("a").find("p",class_="price-sale").find("span",class_="price-regular")
        
        if regular == None:                                                                                                         #Giá gốc
            reprice = "None"
        else:
            reprice = x.find("a").find("p",class_="price-sale").find("span",class_="price-regular").text.strip()
            
        price = conv(x.find("a").find("p",class_="price-sale").find("span",class_="final-price").text.strip().split()[0][:-1])                  # Giá hiện tại

        img = x.find("a").find("img",class_="product-image").get('src').strip()                                                     #link ảnh

        productlink = x.find("a").get('href').strip()                                                                               #link sản phẩm

        name = x.get('data-title').strip()                                                                                          #tênsản phẩm

        if x.get('data-brand') == None :                                                                                            #nhãn hiệu

            brand = "None"
        else:

            brand = x.get('data-brand').strip()

        #price = x.get('data-price').strip()
        category = x.get('data-category').strip()                                                                                   #Thể loại
        if productlink[0]=="/":
            productlink = "https://tiki.vn"+ productlink
        else:
            pass  
        appe = {
            'Tên':[name],
            'Giá cũ':[reprice],
            'Giá mới':[price],
            'Thương hiệu':[brand],
            'Danh mục thể loại':[category],
            'Link ảnh':[img],
            'Link sản phẩm':[productlink]
        }
        df2 = pd.DataFrame(data=appe)   
        df=df.append(df2,ignore_index=True)
        row+=1 
    page = page +1
pr = df['Giá mới']
df.to_excel(keyword+"-Tiki.xlsx")
print('Đã scrap xong tiki')
print('Đang scrap shopee....')


#                                                                           Shopee

recordshopee = {
    'Tên':[],
    'Giá cũ':[],
    'Giá mới':[],
    'Link ảnh':[],
    'Link sản phẩm':[],
    'Nơi bán':[]
}

shopeedf = pd.DataFrame(data=recordshopee)

page = 0
row = 1
path = "C:\\Users\\vnhie\\OneDrive\\Desktop\\Project 2\\e comerce scraping\\chromedriver.exe"
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")
driver = webdriver.Chrome(path,chrome_options=options)
while page < 8:

    driver.get("https://shopee.vn/search?keyword="+keyword+"&page="+str(page))
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/5);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*2/5);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*3/5);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight*4/5);")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'html5lib')

    # truy cập tới từng item:
    mainpage = soup.find("div", id="main")
    itemlistpage = mainpage.find("div", role="main")
    itemframe = itemlistpage.find("div", class_="shopee-search-item-result")
    listitem = itemframe.find("div", class_="row shopee-search-item-result__items")
    if listitem == None:
        break
    items = listitem.find_all("div", class_="col-xs-2-4 shopee-search-item-result__item")

    for x in items:
        if x == None :
            break

        if x.find("div", class_="_1NoI8_") == None:         # name

            name = "None"
        else:

            name = x.find("div", class_="_1NoI8_").string

        if x.find("div", class_="_1w9jLI _37ge-4 _2ZYSiu").find_all("span")[1] == None:             # price
            price = "None"
        else:

            price = conv(x.find("div", class_="_1w9jLI _37ge-4 _2ZYSiu").find_all("span")[1].string)

        if x.find("div", class_="_1w9jLI QbH7Ig U90Nhh") == None:                                       # price 2
            oldprice = "None"
        else:

            oldprice = (x.find("div", class_="_1w9jLI QbH7Ig U90Nhh").string)

        if x.find("img", class_="_1T9dHf _3XaILN") == None:                                           # image
            img = "None"
        else:

            img = x.find("img", class_="_1T9dHf _3XaILN")['src']

        if x.find("a") == None:                                                                           #link
            link = "None"
        else:

            link ="https://shopee.vn/" + x.find("a")['href']

        if x.find("div", class_="_3amru2") == None:                                                    #location
            locate = "None"
        else:

            locate = x.find("div", class_="_3amru2").string
        recordsp = {
                'Tên':name,
                'Giá cũ':oldprice,
                'Giá mới':price,
                'Link ảnh':img,
                'Link sản phẩm':link,
                'Nơi bán':locate  
        }
        shopeedf = shopeedf.append(recordsp,ignore_index=True)
        
        row+=1
    page+=1

  #  print(len(items))
shopeedf.to_excel(keyword+"-shopee.xlsx")
pr = pr.append(shopeedf['Giá mới'])/1000000
plt.title("Bảng phân bố giá liên quan đến từ khóa: "+keyword)
plt.xlabel('Giá (triệu đồng)')
plt.ylabel('Số lượng (chiếc)')
plt.hist(pr,50)
plt.xticks(np.arange(min(pr), max(pr)+1, max(pr)/50 ))
plt.xticks(rotation=45)
plt.grid()
print("Đã scrapt xong shopee")
plt.show()