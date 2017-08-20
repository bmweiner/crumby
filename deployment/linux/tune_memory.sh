# This script will tune mysql and apache memory settings for
# a low memory Amazon Linux AMI 2017.03.1 (HVM), SSD Volume Type.

# configure mysql
cat <<EOF >> /etc/my.cnf

[mysqld]
innodb_buffer_pool_size=32M
innodb_log_buffer_size=256K
key_buffer_size=8
max_connections=10
EOF

# configure apache
cat <<EOF >> /etc/httpd/conf/httpd.conf

<IfModule prefork.c>
    StartServers          3
    MinSpareServers       2
    MaxSpareServers       5
    MaxClients            10
    MaxRequestsPerChild   1000
</IfModule>
EOF

# restart services and enable on restart
service mysqld restart
service httpd restart
