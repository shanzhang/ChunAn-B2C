from django.db import models,connection,transaction

# Create your models here.
def getUserInfo(userName):
    cursor = connection.cursor()
    sql = "SELECT id,username,email,is_superuser,is_staff,is_active FROM auth_user WHERE username = %s"
    data = cursor.execute(sql,[userName]).fetchall()
    connection.close()
    return data[0]