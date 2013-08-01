# Create your models here.
from django.db import connection,transaction
from django.db import models
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_IBAR = '||'
SPLIT_HEAD = '|h|'
SPLIT_LBAR = '^_^'
STATUS_PAID = 1
STATUS_SENT = 2
STATUS_RECEIVED = 3

def loadOrderList(username):
    print "=============== start order ==================="
    cursor = connection.cursor()
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders WHERE user_id = %s order by created_date desc"
    re = cursor.execute(sql,[user_id]).fetchall()
    if re is None:
        connection.close()
        return 0
    data = []
    count = 0
    for row in re:
        order_id = row[0]
        order_number = row[1]
        created_date = row[2]
        state = row[3]
        payment_price = row[4]
        data.append(str(order_number) + SPLIT_SBAR + str(created_date) + SPLIT_SBAR + str(state) + SPLIT_SBAR + str(payment_price) + SPLIT_HEAD)
        sql = "SELECT product_name,price_unit,product_amount,product_id FROM order_item WHERE order_id = %s"
        res = cursor.execute(sql,[order_id]).fetchall()
        i = 0
        for row1 in res:
	        name = row1[0]
	        price_unit = row1[1]
	        amount = row1[2]
	        i = i + 1
	        data.append(str(name) + SPLIT_SBAR + str(price_unit) + SPLIT_SBAR + str(amount) + SPLIT_SBAR + str(row1[3]) + SPLIT_IBAR)
        data.append('&' + str(i) + SPLIT_LBAR)
        count = count +1
    data.append('^&^' + str(count))
    connection.close()
    return data


def pay(username,price1,price2,invoiceTag,invoiceCompany,shippingName,address,city,zipcode,phone,message,province):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT id FROM auth_user WHERE username = %s"
    user_id = str(cursor.execute(sql,[username]).fetchone()[0])
    sql = "INSERT INTO orders VALUES (NULL,%s,%s,%s,%s,NULL,%s,%s,%s,%s,%s,NULL,%s,%s,%s,%s,%s,%s,NULL,NULL,%s)"
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    order_number = str(time.strftime("%Y%m%d%X", time.localtime())).replace(':','') + user_id
    print order_number
    state = STATUS_PAID
    shippingPrice = 6
    if(price1 == price2):
        shippingPrice = 0
    cursor.execute(sql,[order_number,user_id,date_time,state,price1,invoiceTag,invoiceCompany,shippingName,address,city,province,zipcode,phone,shippingPrice,price2,message])
    
    sql = "SELECT order_id FROM orders WHERE order_number = %s"
    order_id = cursor.execute(sql,[order_number]).fetchone()[0]
    sql = "SELECT cart_id FROM cart WHERE user_id = %s"
    cart_id = cursor.execute(sql,[user_id]).fetchone()[0]
    sql = "SELECT product_id,amount FROM cart_item WHERE cart_id = %s"
    re = cursor.execute(sql,[cart_id]).fetchall()
    for row in re:
        product_id = row[0]
        amount = row[1]
        sql = "SELECT name,price,stock_amount,image FROM product WHERE product_id = %s"
        res = cursor.execute(sql,[product_id]).fetchone()
        name  = res[0]
        price_unit = res[1]
        cur_amount = res[2]
        price_total = price_unit * amount
        if cur_amount == 0:
            connection.close()
            return -1
        if cur_amount < amount:
            connection.close()
            return 0
        else:
            cur_amount = cur_amount - amount
        sql = "INSERT INTO order_item VALUES(NULL,%s,%s,%s,%s,%s,%s)"
        cursor.execute(sql,[order_id,price_total,product_id,price_unit,amount,name])
        sql = "UPDATE product SET stock_amount = %s WHERE product_id = %s"
        cursor.execute(sql,[cur_amount,product_id])
        sql = "SELECT COUNT(product_id) FROM sell_record WHERE product_id = %s"
        sell_or_not = cursor.execute(sql,[product_id]).fetchone()[0]
        if sell_or_not == 0:
            sql = "INSERT INTO sell_record VALUES(NULL,%s,%s,%s,%s,%s)"
            cursor.execute(sql,[product_id,price_unit,name,res[3],amount])
        else:
            sql = "UPDATE sell_record SET amount = %s WHERE product_id = %s"
            cursor.execute(sql,[amount,product_id])
    
    sql = "DELETE FROM cart_item WHERE cart_id = %s"
    cursor.execute(sql,[cart_id])
    sql = "DELETE FROM cart WHERE cart_id = %s"
    cursor.execute(sql,[cart_id])

    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return 1

def receiveProduct(oid):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "UPDATE orders SET state = %s WHERE order_number = %s"
    cursor.execute(sql,[STATUS_RECEIVED,oid])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return 1