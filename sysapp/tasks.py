from auto_devops.celery import app




@app.task()
def try_connect_mysql(**kwargs):
    import mysql.connector
    from mysql.connector import errorcode
    from sysapp.models import DbServer
    default_param = {
            'host':'127.0.0.1',
            'user':'root',
            'password':'root',
            'port':3306 ,
            'database':'tmp',
            'charset':'utf8',
            }
    id = kwargs.pop('id', 0)
    mysql_param = {}
    err_res = ''
    for k, v in default_param.iteritems():
        mysql_param[k] = kwargs.pop(k, v)
    try:
        conn = mysql.connector.connect(**mysql_param)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            err_res = "something is wrong with user or password"
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            err_res = "database does not exists"
        DbServer.objects.filter(id=id).update(dbstatus=2)
    else:
        DbServer.objects.filter(id=id).update(dbstatus=1)
    finally:
        conn.close()



