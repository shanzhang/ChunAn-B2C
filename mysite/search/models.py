# Create your models here.
import sys
from django.db import connection
reload(sys)
sys.setdefaultencoding('utf-8')

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def search(query):
    cursor = connection.cursor()
    sql = "SELECT product_id,meta_title,price,image,name,category_id " \
          "FROM product WHERE active = 1 AND stock_amount > 0 " \
          "AND meta_title like  %s" % ('"%%' + '%s' % query + '%%"')
    print sql
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(row[3]) + SPLIT_SBAR + str(row[4]) + SPLIT_SBAR + str(row[5]) + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    print "==============="
    connection.close()
    return data