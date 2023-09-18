def create_group(gid,codis_dashboard_addr):
    _template = "codis-admin --dashboard={dashboard_addr} --create-group --gid={gid}".format(dashboard_addr=codis_dashboard_addr,gid=gid)
    print(_template)

def add_pika_group(gid,codis_dashboard_addr,master,slave):
    add_master = "codis-admin --dashboard={dashboard_addr} --group-add --gid={gid} --addr={master}:9221".format(dashboard_addr=codis_dashboard_addr,gid=gid,master=master)
    add_slave  = "codis-admin --dashboard={dashboard_addr} --group-add --gid={gid} --addr={slave}:9221".format(dashboard_addr=codis_dashboard_addr,gid=gid,slave=slave)
    print(add_master)
    print(add_slave)
   # print(master)
   # print(slave)
## codis-admin --dashboard=172.22.10.107:18080 --rebalance --confirm

def add_tcmalloc(master,slave):
    add_master = "redis-cli -h {master} -p 9221 tcmalloc rate 9 ".format(master=master)
    add_slave  = "redis-cli -h {slave} -p 9221  tcmalloc rate 9 ".format(slave=slave)
    print(add_master)
    print(add_slave)

# def do_command(master,slave,command):
#     add_master = "redis-cli -h {master} -p 9221 {command} ".format(master=master,command=command)
#     add_rewrite_master = "redis-cli -h {master} -p 9221 {command} ".format(master=master,command="config rewrite")
#
#     add_slave  = "redis-cli -h {slave} -p 9221  {command} ".format(slave=slave,command=command)
#     add_rewrite_slave = "redis-cli -h {slave} -p 9221  {command} ".format(slave=slave,command="config rewrite")
#     print(add_master)
#     print(add_rewrite_master)
#     print(add_slave)
#     print(add_rewrite_slave)
def do_command(ip,command):
    add_ip = "redis-cli -h {ip} -p 9221 {command} ".format(ip=ip,command=command)
    add_rewrite_ip = "redis-cli -h {ip} -p 9221 {command} ".format(ip=ip,command="config rewrite")
    print(add_ip)
 #   print(add_rewrite_ip)


if __name__ == '__main__':
    f = open('xxxx/offline_codis.list')
    codis_dashboard_addr="10.100.50.178:18080"
    #command="config get \*"
    #command="config set compact-cron 01-02/20"
    command="SCAN 0 MATCH 1101860_* COUNT 10"
    lines = f.readlines()
    for _line in lines:
       # print(_line)
        gid    = _line.split('\t')[0]
        master = _line.split('\t')[1]
        slave  = _line.split('\t')[2].rstrip('\n')
       # create_group(gid,codis_dashboard_addr)
        add_pika_group(gid,codis_dashboard_addr,master,slave)
        # do_command(slave,"slaveof "+master+":9221")
        # add_tcmalloc(master,slave)
        # do_command(master,command)
        #do_command(slave,command)
    f.close()
