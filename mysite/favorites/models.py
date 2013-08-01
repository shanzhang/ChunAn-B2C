# Create your models here.
from django.db import connection,transaction
from django.db import models
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def addToFav(user_id,pid):
    cursor = connection.cursor()
    connection.close()
    if checkFavExist(user_id) is True:
        updateFav(user_id,pid)
    else:
        insertFav(user_id,pid)

def checkFavExist(user_id):
    cursor = connection.cursor()
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    re = cursor.execute(sql,[user_id]).fetchone()
    if re is None:
        connection.close()
        return False
    else:
        connection.close()
        return True

def updateFav(user_id,pid):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "UPDATE favorites SET modified_date = %s WHERE user_id = %s"
    cursor.execute(sql,[date_time,user_id])
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    fav_id = cursor.execute(sql,[user_id]).fetchone()[0]
    if checkFavItemExist(fav_id,pid,cursor) is True:
        sql = "UPDATE favorites_item SET modification_date = %s WHERE fav_id = %s AND product_id = %s"
        cursor.execute(sql,[date_time,fav_id,pid])
    else:
        sql = "INSERT INTO favorites_item VALUES(NULL,%s,%s,%s,NULL)"
        cursor.execute(sql,[fav_id,pid,date_time])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def checkFavItemExist(fav_id,pid,cursor):
    sql = "SELECT fav_item_id FROM favorites_item WHERE fav_id = %s AND product_id = %s"
    re = cursor.execute(sql,[fav_id,pid]).fetchone()
    if re is None:
        return False
    else:
        return True

def insertFav(user_id,pid):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "INSERT INTO favorites VALUES(NULL,%s,%s,NULL)"
    cursor.execute(sql,[user_id,date_time])
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    fav_id = cursor.execute(sql,[user_id]).fetchone()[0]
    sql = "INSERT INTO favorites_item VALUES(NULL,%s,%s,%s,NULL)"
    cursor.execute(sql,[fav_id,pid,date_time])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def loadFav(user_id):
    cursor = connection.cursor()
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    fav_id = cursor.execute(sql,[user_id]).fetchone()
    if fav_id is None :
        return 0
    else:
        fav_id = fav_id[0]
        sql = "SELECT product_id,name,price,image FROM product WHERE product_id in (SELECT product_id FROM favorites_item WHERE fav_id = %s)"
        re = cursor.execute(sql,[fav_id]).fetchall()
        data  = []
        i = 0
        for row in re:
            data.append(str(row[0]) + SPLIT_SBAR + row[1] + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + row[3] + SPLIT_LBAR)
            i = i + 1
        data.append('&' + str(i))
        connection.close()
        return data

def delFav(user_id):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    fav_id = cursor.execute(sql,[user_id]).fetchone()[0]
    sql = "DELETE FROM favorites_item WHERE fav_id = %s"
    cursor.execute(sql,[fav_id])
    sql = "DELETE FROM favorites WHERE fav_id = %s"
    cursor.execute(sql,[fav_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def delFavItem(user_id,product_id):
    is_empty = 0
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT fav_id FROM favorites WHERE user_id = %s"
    fav_id = str(cursor.execute(sql,[user_id]).fetchone()[0])
    sql = "DELETE FROM favorites_item WHERE fav_id = %s AND product_id = %s"
    cursor.execute(sql,[fav_id,product_id])
    sql = "SELECT COUNT(product_id) FROM favorites_item WHERE fav_id = %s"
    count = cursor.execute(sql,[fav_id]).fetchone()[0]
    if count == 0:
        sql = "DELETE FROM favorites WHERE fav_id = %s"
        cursor.execute(sql, [fav_id])
        is_empty = 1
    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return is_empty

def getFav(user_id):
    cursor = connection.cursor()
    sql = "SELECT COUNT(fav_id) FROM favorites WHERE user_id = %s"
    re = cursor.execute(sql,[user_id]).fetchone()[0]
    if re == 0:
        return 1
        connection.close()
    else:
        return 0
        connection.close()