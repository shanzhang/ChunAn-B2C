import sys
from django.db import connection
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def getCategory():
    cursor = connection.cursor()
    sql = "SELECT category_id,parent_id,level,description FROM category"
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        print row
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + row[3] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def category_product(offset):
    cursor = connection.cursor()
    sql = "SELECT product_id,meta_title,price,image,name FROM product WHERE category_id = %s AND active = 1"
    print sql
    re = cursor.execute(sql,[offset]).fetchall()
    data  = []
    i = 0
    for row in re:
        print row
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + row[3] + SPLIT_SBAR + row[4] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def loadAllProduct():
    cursor = connection.cursor()
    sql = "SELECT product_id,meta_title,price,image,name FROM product WHERE active = 1"
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        print row
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + row[3] + SPLIT_SBAR + row[4] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data