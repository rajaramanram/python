
select_port='10.227.45.122'
dict_server={
    '10.227.45.103':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.104':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.105':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.106':"hostname ; systemctl status nagios ; systemctl status crond",
    '10.227.45.107':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.108':"hostname ; systemctl status mod-gearman-worker",
    '10.227.45.109':"hostname ; systemctl systemctl status mod-gearman-worker",
    '10.227.45.110':"hostname ; systemctl status nagios ; systemctl status mod-gearman-worker",
    '10.227.45.114':"hostname ; systemctl status postgresql-9.6 ; systemctl status mongod",
    '10.227.45.124':"hostname ; systemctl status mariadb",
    '10.227.45.122':"hostname ; systemctl status nfsd ; systemctl status rabbitmq-server",
    '10.227.45.121':"hostname ; systemctl status rabbitmq-server ; ps -ef|grep elasticsearch.bootstrap|grep -v grep",
    '10.227.45.123':"hostname ; systemctl status rabbitmq-server",
    '10.227.45.119':"hostname ; service kibana status",
    '10.227.45.120':"ps -ef|grep elasticsearch.bootstrap|grep -v grep",
    }.get(select_port)
print(dict_server)

    
    
