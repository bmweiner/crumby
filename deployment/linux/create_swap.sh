# This script will create a swap file for Amazon Linux AMI 2017.03.1 (HVM), SSD
# Volume Type.

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
