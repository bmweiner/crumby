# This script will add a swap file and tweak mysql and apache settings for
# a low memory Amazon Linux AMI 2017.03.1 (HVM), SSD Volume Type.

# setup swap file
fallocate -l 1G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile

# mount swapfile on boot
cat <<EOF >> /etc/fstab
/swapfile   swap    swap    sw  0   0
EOF

# set swappiness and cache pressure
cat <<EOF >> /etc/sysctl.conf

# Lower swappiness and cache pressure for low-memory vps
vm.swappiness = 10
vm.vfs_cache_pressure=50
EOF

# apply parameter settings
sysctl -p

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
