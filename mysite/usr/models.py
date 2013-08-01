from django.db import models
from django.db import connection,transaction

# Create your models here.
def getAllUsers():
    cursor = connection.cursor()
    sql = "SELECT username,email,is_staff,is_active,is_superuser,last_login,date_joined FROM auth_user " 
    print sql
    data = cursor.execute(sql).fetchall()
    connection.close()
    return data