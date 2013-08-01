# Create your models here
import sys
from django.db import connection
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def detail_display(offset):
    cursor = connection.cursor()
    sql = "SELECT * FROM product WHERE product_id = %s"
    re = cursor.execute(sql,[offset]).fetchall()
    data  = {}.fromkeys(('product_id', 'name','price','desc','title','stock_amount','image'))
    for row in re:
        data['product_id'] = str(row[0])
        data['name'] = row[1]
        data['price'] = str(row[2])
        data['desc'] = row[4]
        data['title'] = row[6]
        data['stock_amount'] = str(row[8])
        data['image'] = row[10]
        data['image1'] = row[10].split('.jpg')[0] + 'b.jpg'
        data['category'] = str(row[3])
    connection.close()
    return data

def loadCompare(cate,myId):
    cursor = connection.cursor()
    sql = "SELECT product_id,meta_title,price,image,name FROM product " \
          "WHERE active = 1 AND stock_amount > 0 AND category_id = %s AND product_id != %s"
    re = cursor.execute(sql,[cate,myId]).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(row[3]) + SPLIT_SBAR + str(row[4]) + SPLIT_LBAR)
        i = i + 1
        if i >= 6 :
            break
    data.append('&' + str(i))
    connection.close()
    return data

def loadNewOn(myId):
    cursor = connection.cursor()
    sql = "SELECT product_id,meta_title,price,image,name FROM product " \
          "WHERE active = 1 AND stock_amount > 0 AND product_id != %s ORDER BY creation_date desc"
    re = cursor.execute(sql,[myId]).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(row[3]) + SPLIT_SBAR + str(row[4]) + SPLIT_LBAR)
        i = i + 1
        if i >= 6 :
            break
    data.append('&' + str(i))
    connection.close()
    return data