import psycopg2
from psycopg2 import pool
try:
    postgreSQL_pool = psycopg2.pool.SimpleConnectionPool(1, 20, user="postgres",
        password="rajaraman",host="127.0.0.1",port="5432",database="customer_metadata")
    if(postgreSQL_pool):
        print("Connection pool created successfully")

    # Use getconn() to Get Connection from connection pool
    ps_connection = postgreSQL_pool.getconn()

    if(ps_connection):
        print("successfully recived connection from connection pool ")
        ps_cursor = ps_connection.cursor()
        ps_cursor.execute("select * from cusotmer_secret where sub_domain = 'customer_c'")
        alert_records = ps_cursor.fetchall()
        print(alert_records)
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
        #print("Displaying rows from mobile table")
        '''for row in alert_records:
            print(row)
            for i in row:
                print(i)'''
        

        ps_cursor.close()

        #Use this method to release the connection object and send back to connection pool
        postgreSQL_pool.putconn(ps_connection)
        print("Put away a PostgreSQL connection")

except (Exception, psycopg2.DatabaseError) as error:
    print("Error while connecting to PostgreSQL", error)

finally:
    #closing database connection.
    # use closeall method to close all the active connection if you want to turn of the application
    if (postgreSQL_pool):
        postgreSQL_pool.closeall
    print("PostgreSQL connection pool is closed")
