import psycopg2
from psycopg2 import pool
postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
        password="rajaraman", host="127.0.0.1", port="5432", database="customer_metadata")
if(postgreSQL_pool):
    print("Connection pool created successfully")

ps_connection = postgreSQL_pool.getconn()

if(ps_connection):
    ps_cursor = ps_connection.cursor()
    ps_cursor.execute("select * from cusotmer_secret where sub_domain = 'customer_c'")
    alert_records = ps_cursor.fetchall()
    #print(alert_records)
    web_urls = {
            "web": {
                "issuer": alert_records[0][2],
                "auth_uri": alert_records[0][3],
                "client_id": alert_records[0][4],
                "client_secret": alert_records[0][5],
                "redirect_uris": alert_records[0][6],
                "userinfo_uri": alert_records[0][7],
                "token_uri": alert_records[0][8],
                "token_introspection_uri": alert_records[0][9]
            }
        }
    print(web_urls)
        
ps_cursor.close()
