# Create your models here.
import time
import sys
from django.db import connection,transaction
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'
SPLIT_IBAR = '||'
SPLIT_HEAD = '|h|'
STATUS_PAID = 1
STATUS_SENT = 2
STATUS_RECEIVED = 3

def getCategory():
    cursor = connection.cursor()
    sql = "SELECT category_id,description FROM category"
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + row[1] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def addCategory(parent,son):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    if parent == '0':
        level = 0
    else:
        sql = "SELECT level FROM category WHERE category_id = %s"
        level = cursor.execute(sql,[parent]).fetchone()[0] + 1
    sql = "INSERT INTO category VALUES (NULL,%s,%s,%s);"
    # Print_Debug_Param(sql)
    cursor.execute(sql,[parent,level,son])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def deleteCategory(category_id):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "SELECT COUNT(category_id) FROM category WHERE parent_id = %s"
    re = cursor.execute(sql,[category_id]).fetchone()[0]
    if re != 0:
        connection.close()
        return 0
    sql = "SELECT COUNT(product_id) FROM product WHERE category_id = %s"
    re = cursor.execute(sql,[category_id]).fetchone()[0]
    if re != 0:
        connection.close()
        return 0
    sql = "DELETE FROM category WHERE category_id = %s"
    cursor.execute(sql,[category_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return 1

def modifyCategory(parent,cur_cate,son):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    if parent == '0':
        level = 0
    else:
        sql = "SELECT level FROM category WHERE category_id = %s"
        level = cursor.execute(sql,[parent]).fetchone()[0] + 1
    sql = "UPDATE category SET description = %s,parent_id = %s,level = %s " \
          "WHERE category_id = %s"
    # Print_Debug_Param(sql)
    cursor.execute(sql,[son,parent,level,cur_cate])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def loadLeafCategory():
    cursor = connection.cursor()
    sql = "SELECT category_id,description FROM category WHERE category_id NOT IN (SELECT DISTINCT(parent_id) FROM category)"
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + row[1] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def addProduct(cate,name,price,desc,keywords,title,active,amount,image):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "INSERT INTO product VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);"
    # Print_Debug_Param(sql)
    cursor.execute(sql,[name,price,cate,desc,keywords,title,active,amount,date_time,image])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def loadProduct(cate):
    cursor = connection.cursor()
    sql = "SELECT product_id,name FROM product WHERE category_id = %s"
    re = cursor.execute(sql,[cate]).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + row[1] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def loadProductInfo(pid):
    cursor = connection.cursor()
    sql = "SELECT name,price,description,meta_keywords,meta_title,stock_amount,image FROM product WHERE product_id = %s"
    re = cursor.execute(sql,[pid]).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + row[2] + SPLIT_SBAR + row[3] + SPLIT_SBAR + row[4]+ SPLIT_SBAR + str(row[5]) + SPLIT_SBAR + row[6] + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    if(i!=1):
        raise Http404
    connection.close()
    return data

def deleteProduct(product_id):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "DELETE FROM product WHERE product_id = %s"
    cursor.execute(sql,[product_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def modifyProduct(product_id,cate,name,price,desc,keywords,title,active,amount,image):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d", time.localtime())
    sql = "UPDATE product SET name = %s, price = %s, category_id = %s, description = %s, meta_keywords = %s, meta_title = %s,active = %s,stock_amount = %s,creation_date = %s,image = %s" \
          " WHERE product_id = %s"
    # Print_Debug_Param(sql)
    cursor.execute(sql,[name,price,cate,desc,keywords,title,active,amount,date_time,image,product_id])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()

def search_product(query):
    cursor = connection.cursor()
    sql = "SELECT product_id,name,category_id FROM product WHERE meta_keywords like  %s" % ('"%%' + '%s' % query + '%%"')
    re = cursor.execute(sql).fetchall()
    if re is None:
        connection.close()
        return 0
    data  = []
    i = 0
    for row in re:
        sql = "SELECT description FROM category WHERE category_id = %s"
        cname = cursor.execute(sql,[row[2]]).fetchone()[0]
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(cname) + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def loadOrderAdmin():
    cursor = connection.cursor()
    sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders WHERE state = %s order by created_date desc"
    re = cursor.execute(sql,[STATUS_PAID]).fetchall()
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

def loadAllOrderAdmin():
    cursor = connection.cursor()
    sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders order by created_date desc"
    re = cursor.execute(sql).fetchall()
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

def sendProduct(oid):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    sql = "UPDATE orders SET state = %s, state_modified_date = %s WHERE order_number = %s"
    cursor.execute(sql,[STATUS_SENT,date_time,oid])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return 1

def searchOrderAdmin(query,search_type,start,end):
    cursor = connection.cursor()
    if search_type == 'byId':
        sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders WHERE order_number = %s or order_number = %s order by created_date desc"
        re = cursor.execute(sql,[query,int(query) *(-1)]).fetchall()
    if search_type == 'byName':
        sql = "SELECT id FROM auth_user WHERE username = %s"
        user_id = cursor.execute(sql,[query]).fetchone()[0]
        sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders WHERE user_id = %s order by created_date desc"
        re = cursor.execute(sql,[user_id]).fetchall()
    if search_type == 'byTime':
        sql = "SELECT order_id,order_number,created_date,state,payment_price FROM orders WHERE datetime(created_date) >= %s AND datetime(created_date) <= %s order by created_date desc"
        re = cursor.execute(sql,[start,end]).fetchall()
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

def getUser(types,keywords):
    cursor = connection.cursor()

    if(types=="account"):
        sql="SELECT id,username,email,is_staff,is_superuser,is_active,strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(last_login,'localtime')),strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(date_joined,'localtime')) FROM auth_user WHERE username = %s"
    elif(types=="id"):
        sql="SELECT id,username,email,is_staff,is_superuser,is_active,strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(last_login,'localtime')),strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(date_joined,'localtime')) FROM auth_user WHERE id = %s"
    else:
        sql="SELECT id,username,email,is_staff,is_superuser,is_active,strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(last_login,'localtime')),strftime('%%Y-%%m-%%d %%H:%%M:%%S', datetime(date_joined,'localtime')) FROM auth_user WHERE email = %s"


    re = cursor.execute(sql,[keywords]).fetchall()

    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(row[3]) + SPLIT_SBAR + str(row[4]) + SPLIT_SBAR + str(row[5]) + SPLIT_SBAR + str(row[6]) + SPLIT_SBAR + str(row[7]) + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data

def activateUser(uid,is_active):
    status = 0
    if(is_active=="True"):
        sql="UPDATE auth_user SET is_active=%s WHERE id=%s"
        status = 0
    if(is_active=="False"):
        sql="UPDATE auth_user SET is_active=%s WHERE id=%s"
        status = 1
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    cursor.execute(sql,[status,uid])
    if transaction.is_dirty():
        transaction.commit()
    return 1

def adminUser(uid,is_active):
    status = 0
    if(is_active=="True"):
        sql="UPDATE auth_user SET is_superuser=%s WHERE id=%s"
        status = 0
    if(is_active=="False"):
        sql="UPDATE auth_user SET is_superuser=%s WHERE id=%s"
        status = 1
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    cursor.execute(sql,[status,uid])
    if transaction.is_dirty():
        transaction.commit()
    return 1