import sys
from django.db import connection
reload(sys)
sys.setdefaultencoding('utf-8')
# Create your models here.

SPLIT_SBAR = '|'
SPLIT_LBAR = '^_^'

def market_display():
    cursor = connection.cursor()
    sql = "SELECT product_id,price,name,image,amount FROM sell_record ORDER BY amount desc"
    re = cursor.execute(sql).fetchall()
    data  = []
    i = 0
    for row in re:
        if i >= 15:
            break
        data.append(str(row[0]) + SPLIT_SBAR + str(row[1]) + SPLIT_SBAR + str(row[2]) + SPLIT_SBAR + str(row[3]) + SPLIT_SBAR + str(row[4]) + SPLIT_LBAR)
        i = i + 1
    data.append('&' + str(i))
    connection.close()
    return data