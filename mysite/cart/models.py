# Create your models here.
from django.db import connection,transaction
from django.db import models
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def addToCart(username,pid,amount):
    print "=============== start add to cart ==================="
    cursor = connection.cursor()
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    connection.close()
    if checkCartExist(user_id) is True:
        updateCart(user_id,pid,amount)
    else:
        insertCart(user_id,pid,amount)

def checkCartExist(user_id):
    cursor = connection.cursor()
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    re = cursor.execute(sql,[user_id]).fetchone()
    connection.close()
    if re is None:
        return False
    else:
        return True

def updateCart(user_id,pid,amount):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "UPDATE cart SET modified_date = %s WHERE user_id = %s"
    cursor.execute(sql,[date_time, user_id])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = cursor.execute(sql,[user_id]).fetchone()[0]
    if checkCartItemExist(cart_id,pid,cursor) is True:
        print "============== start update cart_item =============="
        sql = "UPDATE cart_item SET amount = %s, modified_date = %s " \
              "WHERE cart_id = %s AND product_id = %s"
        cursor.execute(sql,[amount, date_time, cart_id, pid])
    else:
        print "============== start insert into cart_item =============="
        sql = "INSERT INTO cart_item " \
              "VALUES(NULL,%s,%s,%s,%s,NULL)"
        cursor.execute(sql, [cart_id, pid, amount, date_time])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def checkCartItemExist(cart_id,pid,cursor):
    sql = "SELECT cart_item_id FROM cart_item " \
          "WHERE cart_id = %s AND product_id = %s"
    re = cursor.execute(sql,[cart_id, pid]).fetchone()
    if re is None:
        return False
    else:
        return True

def insertCart(user_id,pid,amount):
    print "=============== start insert into cart ==================="
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "INSERT INTO cart VALUES(NULL,%s,%s,NULL)"
    cursor.execute(sql,[user_id,date_time])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = cursor.execute(sql,[user_id]).fetchone()[0]
    sql = "INSERT INTO cart_item VALUES(NULL,%s,%s,%s,%s,NULL)"
    cursor.execute(sql,[cart_id, pid, amount, date_time])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def delCart(username):
    print "=============== start delete into cart ==================="
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = cursor.execute(sql,[user_id]).fetchone()[0]
    sql = "DELETE FROM cart_item WHERE cart_id = %s"
    cursor.execute(sql,[cart_id])
    sql = "DELETE FROM cart WHERE user_id = %s"
    cursor.execute(sql,[user_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def loadCart(username):
    cursor = connection.cursor()
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = cursor.execute(sql,[username]).fetchone()[0]
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = cursor.execute(sql,[user_id]).fetchone()
    if cart_id is None :
        return 0
    else:
        cart_id = cart_id[0]
        sql = "SELECT product_id,name,price,image FROM product " \
              "WHERE product_id in " \
              "(SELECT product_id FROM cart_item WHERE cart_id = %s)"
        re = cursor.execute(sql,[cart_id]).fetchall()
        data  = []
        i = 0
        for row in re:
            sql = "SELECT amount FROM cart_item WHERE cart_id = %s AND product_id = %s"
            amount = cursor.execute(sql,[cart_id,row[0]]).fetchone()[0]
            sql = "SELECT stock_amount FROM product WHERE product_id = %s"
            cur_amount = cursor.execute(sql,[row[0]]).fetchone()[0]
            if amount > cur_amount:
                amount = cur_amount
            data.append(str(row[0]) + SPLIT_SBAR + row[1] + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + row[3] + SPLIT_SBAR + str(amount) + SPLIT_LBAR)
            i = i + 1
        data.append('&' + str(i))
        connection.close()
        return data

def getCart(username):
    if username == '' or username is None:
        print "=========== No user is Online ============="
        return 0
    cursor = connection.cursor()
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    re = cursor.execute(sql,[user_id]).fetchone()
    if re is None:
        connection.close()
        return 0
    else:
        cart_id = str(re[0])
        sql = "SELECT COUNT(cart_item_id) FROM cart_item WHERE cart_id = " + cart_id
        count = cursor.execute(sql).fetchone()[0]
        connection.close()
        return count

def delCartItem(username,product_id):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = str(cursor.execute(sql,[user_id]).fetchone()[0])
    sql = "DELETE FROM cart_item WHERE cart_id = %s AND product_id = %s"
    cursor.execute(sql,[cart_id,product_id])
    sql = "SELECT COUNT(product_id) FROM cart_item WHERE cart_id = %s"
    count = cursor.execute(sql,[cart_id]).fetchone()[0]
    if count == 0:
        sql = "DELETE FROM cart WHERE cart_id = %s"
        cursor.execute(sql, [cart_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def updateCartItem(username,product_id,amount):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = str(cursor.execute(sql,[user_id]).fetchone()[0])

    sql = "SELECT stock_amount FROM product WHERE product_id = %s"
    max_amount = str(cursor.execute(sql,[product_id]).fetchone()[0])
    if float(amount) > float(max_amount):
        amount = str(max_amount)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "UPDATE cart_item SET amount = %s ,modified_date = %s WHERE cart_id = %s AND product_id = %s"
    cursor.execute(sql,[amount,date_time,cart_id,product_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()