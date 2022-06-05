---
layout: default
title: Add new work node to existing ECS cluster
nav_order: 3
parent: Operations
grand_parent: Data Service
---

# Add new work node to existing ECS cluster
{: .no_toc }

- TOC
{:toc}

---

## 1. create new work node

- Ensure that ECS master node is up and running. Create a new virtual machine with CentOS-7.9 as base image with the same ip address. Use below commands on openstack plateform.
```
openstack server create \
  --image CentOS-7.9 \
  --flavor  m5.4xlarge \
  --security-group default \
  --availability-zone SE_PERF \
  --key-name id_rsa \
  --port=osft-nw-port-10-113-207-146 \
  --user-data files/user-data.sh \
  feng-ws6
```
We will use this machine as new worker node. 

- Open SSH terminal for new worker node and change hostname the same as your failed node. 
```
hostnamectl set-hostname feng-ws6.sme-feng.athens.cloudera.com
```

- Create a new user to run commands on work node. Give sudo access to this user. Give same username as master node.
```
useradd cloudera
echo cloudera > passwd.txt
echo cloudera >> passwd.txt
passwd cloudera < passwd.txt
echo "cloudera   ALL=(ALL)    NOPASSWD: ALL" >> /etc/sudoers
sed -i 's/^#PasswordAuthentication/PasswordAuthentication/' /etc/ssh/sshd_config
systemctl restart sshd
```

- Add the work node as a new DNS entry into AD domain.

- Modify the resolv.conf file
```
chattr -i /etc/resolv.conf
echo "search sme-feng.athens.cloudera.com
nameserver 10.113.240.31
nameserver 10.113.240.13" > /etc/resolv.conf
chattr +i /etc/resolv.conf
```

- Mount the additional disk /dev/vdc
```
mkfs.xfs -f /dev/vdc
blkid /dev/vdc
echo "/dev/vdc    /mnt2   xfs defaults    0   0" >> /etc/fstab
mkdir -p /mnt2
mount -a
lsblk
```


## 2. Setting Linux Kernel Parameter

- Set the default timezone
```
timedatectl set-timezone "Asia/Shanghai"
```
- Disable selinux
```
setenforce 0
sed -i 's/SELINUX=.*/SELINUX=disabled/' /etc/selinux/config
```

- Set the value of the vm.swappiness parameter for minimum swapping
```
sysctl -a | grep vm.swappiness
echo 1 > /proc/sys/vm/swappiness
sysctl vm.swappiness=1
```

- Disable Transparent Hugepages (THP)
```
echo never > /sys/kernel/mm/transparent_hugepage/enabled
echo never > /sys/kernel/mm/transparent_hugepage/defrag
echo "echo never > /sys/kernel/mm/transparent_hugepage/enabled" >> /etc/rc.d/rc.local
echo "echo never > /sys/kernel/mm/transparent_hugepage/defrag" >> /etc/rc.d/rc.local
```

- Increase entropy by installing rng-tools and starting the rngd service
```
yum -y install rng-tools
rngd -f -v
systemctl restart rngd
systemctl status rngd
systemctl enable rngd
```
- You can check the available entropy by running the following command
```
cat /proc/sys/kernel/random/entropy_avail
```

- change the default soft or hard limit for the number of users processes
```
sed -i 's/4096/65536/' /etc/security/limits.d/20-nproc.conf
```





