service_names=['Nagios is active(running)','Gearmand','Mod-gearman-worker(running)','Npcd is running']
for i in service_names:
    if i.endswith("(running)"):
        print(i)
