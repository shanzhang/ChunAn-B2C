from django.db import models
from django.db import connection,transaction
import time
import sys 
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.


class Groupon(models.Model):
    """
   A totally groupOn product separate from product
   """
    gpid = models.IntegerField()
    name = models.CharField(max_length=50)
    amount = models.IntegerField()
    sell_amount = models.IntegerField()
    price = models.FloatField()
    net_price = models.FloatField()
    description = models.TextField()
    begin_date = models.DateTimeField()
    end_date = models.DateTimeField()
    image = models.CharField(max_length=80)

    def __unicode__(self):
        return "%s" % self.gpid

def gPay(gpid,price,shippingName,address,city,zipcode,phone,province,amount,user_id,gid):
    cursor = connection.cursor()
    transaction.enter_transaction_management()
    transaction.managed(True)
    sql = "INSERT INTO orders VALUES (NULL,%s,%s,%s,%s,NULL,%s,NULL,NULL,%s,%s,NULL,%s,%s,%s,%s,%s,%s,NULL,NULL,NULL)"
    date_time = time.strftime("%Y-%m-%d %X", time.localtime())
    order_number = '-' + str(time.strftime("%Y%m%d%X", time.localtime())).replace(':','') + str(user_id)
    state = 1
    shippingPrice = 0
    cursor.execute(sql,[order_number,user_id,date_time,state,price,shippingName,address,city,province,zipcode,phone,shippingPrice,float(price)*float(amount)])
    sql = "SELECT order_id FROM orders WHERE order_number = %s"
    order_id = cursor.execute(sql,[order_number]).fetchone()[0]
    if gpid == '0' :
        sql = "SELECT name FROM groupon_groupon WHERE id = %s"
        product_name = cursor.execute(sql,[gid]).fetchone()[0]
    else:
        sql = "SELECT name FROM product WHERE product_id = %s"
        product_name = cursor.execute(sql,[gpid]).fetchone()[0]
    sql = "INSERT INTO order_item VALUES (NULL,%s,%s,%s,%s,%s,%s)"
    price_unit = float(price)/float(amount)
    cursor.execute(sql,[order_id,price,gpid,price_unit,amount,product_name])
    sql = "UPDATE groupon_groupon SET amount = amount - %s, sell_amount = sell_amount + %s WHERE gpid = %s"
    cursor.execute(sql,[amount,amount,int(gpid)*(-1)])
    if transaction.is_dirty():
        transaction.commit()
    connection.close()
    return 1