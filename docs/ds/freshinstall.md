---
layout: default
title: Fresh install of ECS 1.3.4 HA Cluster
nav_order: 1
parent: Operations
grand_parent: Data Service
---

# Installing ECS 1.3.4 HA cluster
{: .no_toc }

- TOC
{:toc}

---

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7|
|CM version |Cloudera Manager 7.5.5|
|ECS version |CDP PvC DataServices 1.3.4|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |No, using manual TLS|
|Docker repository options |embedded Docker Repository|
|Databases options |external existing databases|

|IP addresss |hostname |description|
|10.113.207.140	|feng-base.sme-feng.athens.cloudera.com |CDP Base cluster only a single node|
|10.113.207.141	|feng-ws1.sme-feng.athens.cloudera.com |ECS master node 1|
|10.113.207.142	|feng-ws2.sme-feng.athens.cloudera.com |ECS master node 2|
|10.113.207.143	|feng-ws3.sme-feng.athens.cloudera.com |ECS master node 3|
|10.113.207.144	|feng-ws4.sme-feng.athens.cloudera.com |ECS worker node 1|
|10.113.207.145	|feng-ws5.sme-feng.athens.cloudera.com |ECS worker node 2|
|10.113.207.146	|feng-ws6.sme-feng.athens.cloudera.com |ECS worker node 3|

## 2. Install CDP Private Cloud Base Cluster

- Base Cluster is deployed by [Cloudera-Deploy playbook](https://github.com/cloudera-labs/cloudera-deploy.git)

- 6 ECS hosts are available, added to Cloudera Manager but not yet bound to any cluster. In this case `feng-ws[1-6].sme-feng.athens.cloudera.com`

![](../../assets/images/ds/adddns00.png)

## 3. Add DNS records

|hostname|subdomain|Expected roles|DNS ForwardZone|Reverse Zone PTR|
|Wildcard (hostname = *)|apps.ecs-lb.`subdomain`|The string `apps` is required, `ecs-lb` is up to user|Virtual app domain wildcard , `A Record` wildcard (hostsname = *) , Resolves to fixed IP of ha_proxy|N|
|`apps alias`|apps.ecs-lb.`subdomain`|Virtual app domain Alias|CNAME Alias points to `A Record` of ha_proxy. Alternatively can be an ARecord with IP of ha_proxy|N/A|
|ha_proxy|`subdomain`|HA Load balancer|Depends on vendor/software||
|ecs-master1|`subdomain`|ECS Server 1 & Docker server|`A Record` resolves to IP of ecs-master1|Y|
|ecs-master2|`subdomain`|ECS Server 2 & Docker server|`A Record` resolves to IP of ecs-master2|Y|
|ecs-master3|`subdomain`|ECS Server 3 & Docker server|`A Record` resolves to IP of ecs-master3|Y|
|ecs-agentN|`subdomain`|ECS Agent N & Docker server N|`A Record` resolves to IP of ecs-agentN|Y|

- ecs-lb.sme-feng.athens.cloudera.com is the name of this new subdomain. Full name should not exceed 29 chars.

![](../../assets/images/ds/adddns01.png)

- Create a nested subdomain named apps in esc-lb domain.

![](../../assets/images/ds/adddns02.png)

- Define a wildcard `A Record` pointing to the HAProxy host ip address inside `apps` subdomain.
    - Any dns lookups for both apps.ecs-lb.sme-feng.athens.cloudera.com and *.apps.ecs-lb.sme-feng.athens.cloudera.com will resolve to the IP address of HAProxy host.

![](../../assets/images/ds/adddns03.png)

**_NOTE:_** Properties of the host `A Record` inside apps subdomain, note host = asterisk char (*) and that PTR is NOT checked as we dont want to create a reverse lookup for this a-record.

- Run nslookup to check DNS records.

```bash 
hosts="apps.ecs-lb.sme-feng.athens.cloudera.com
*.apps.ecs-lb.sme-feng.athens.cloudera.com
feng-base.sme-feng.athens.cloudera.com
feng-ws1.sme-feng.athens.cloudera.com
feng-ws2.sme-feng.athens.cloudera.com
feng-ws3.sme-feng.athens.cloudera.com
feng-ws4.sme-feng.athens.cloudera.com
feng-ws5.sme-feng.athens.cloudera.com
feng-ws6.sme-feng.athens.cloudera.com
10.113.207.140
10.113.207.141
10.113.207.142
10.113.207.143
10.113.207.144
10.113.207.145
10.113.207.146"

for target in $hosts; do
    nslookup $target
done
```

## 4. Install HAProxy

- ssh to the HAProxy host and install/config haproxy.

    - Example uses a single instance of HAProxy, configured with round robin balancing and tcp mode (allows for non-terminating https).

```bash 
yum install haproxy -y

cat > /etc/haproxy/haproxy.cfg  << EOF
global
    log         127.0.0.1 local2
    chroot      /var/lib/haproxy
    pidfile     /var/run/haproxy.pid
    user        haproxy
    group       haproxy
    daemon

defaults
    mode                    tcp
    log                     global
    option                  tcplog
    option                  dontlognull
    option                  redispatch
    retries                 3
    maxconn                 5000
    timeout connect         5s
    timeout client          50s
    timeout server          50s

listen stats
    bind *:8081
    mode http
    stats enable
    stats refresh 30s
    stats uri /stats
    monitor-uri /healthz

frontend fe_k8s_80
    bind *:80
    default_backend be_k8s_80

backend be_k8s_80
    balance roundrobin
    mode tcp
    server feng-ws1.sme-feng.athens.cloudera.com 10.113.207.141:80 check
    server feng-ws2.sme-feng.athens.cloudera.com 10.113.207.142:80 check
    server feng-ws3.sme-feng.athens.cloudera.com 10.113.207.143:80 check

frontend fe_k8s_443
    bind *:443
    default_backend be_k8s_443

backend be_k8s_443
    balance roundrobin
    mode tcp
    server feng-ws1.sme-feng.athens.cloudera.com 10.113.207.141:443 check
    server feng-ws2.sme-feng.athens.cloudera.com 10.113.207.142:443 check
    server feng-ws3.sme-feng.athens.cloudera.com 10.113.207.143:443 check

EOF

systemctl enable haproxy
systemctl restart haproxy
systemctl status haproxy
```

- You can view [HAproxy UI](http://10.113.207.147:8081/stats) now.


## 5. Create external databases for ECS Cluster

```bash
sudo -u postgres psql << EOF
CREATE ROLE pvc LOGIN PASSWORD 'changeme';
ALTER USER pvc CREATEDB;
DROP DATABASE IF EXISTS "db-env";
DROP DATABASE IF EXISTS "db-mlx";
DROP DATABASE IF EXISTS "db-dwx";
DROP DATABASE IF EXISTS "db-liftie";
DROP DATABASE IF EXISTS "db-ums";
DROP DATABASE IF EXISTS "db-dex";
DROP DATABASE IF EXISTS "db-resourcepoolmanager";
DROP DATABASE IF EXISTS "db-clusteraccessmanager";
DROP DATABASE IF EXISTS "db-alerts";
DROP DATABASE IF EXISTS "cm-registration";
DROP DATABASE IF EXISTS "cluster-proxy";
DROP DATABASE IF EXISTS "db-das";
DROP DATABASE IF EXISTS "db-hue";
CREATE DATABASE "db-env" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-mlx" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-dwx" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-liftie" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-ums" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-dex" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-resourcepoolmanager" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-clusteraccessmanager" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-alerts" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "cm-registration" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "cluster-proxy" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-das" OWNER pvc  ENCODING 'UTF8';
CREATE DATABASE "db-hue" OWNER pvc  ENCODING 'UTF8';
EOF
```

## 6. Install ECS HA cluster

- In Cloudera Manager, on the top right corner, click Add > Add Cluster. In the Select Cluster Type page, select the cluster type as Private Cloud Containerized Cluster and click Continue.

![](../../assets/images/ds/freshinstall00.png)

- On the Getting Started page of the installation wizard, select Internet Install Method. To use a custom repository link provided to you by Cloudera, click Custom Repository. Click Continue.

![](../../assets/images/ds/freshinstall01.png)

- In the Cluster Basics page, type a name for the Private Cloud cluster that you want to create in the Cluster Name field. From the Base Cluster drop-down list, select the cluster that has the storage and SDX services that you want this new Private Cloud Data Services instance to connect with. Click Continue.

![](../../assets/images/ds/freshinstall02.png)

- In the Specify Hosts page, provide a list of available hosts or you can add new hosts. You can provide the Fully Qualified Domain Name (FQDN) in the following patterns:
You can specify multiple addresses and address ranges by separating them by commas, semicolons, tabs, or blank spaces, or by placing them on separate lines. Use this technique to make more specific searches instead of searching overly wide ranges.

![](../../assets/images/ds/freshinstall03.png)

- In the Assign Roles page, you can customize the roles assignment for your new Private Cloud Containerized cluster.
- 6 docker servers - example `feng-ws[1-6].sme-feng.athens.cloudera.com`

![](../../assets/images/ds/freshinstall04.png)

- 3 ECS server - example `feng-ws[1-3].sme-feng.athens.cloudera.com`

![](../../assets/images/ds/freshinstall05.png)

- 3 ECS agents - example `feng-ws[4-6].sme-feng.athens.cloudera.com`

![](../../assets/images/ds/freshinstall06.png)

- Click Continue.

![](../../assets/images/ds/freshinstall07.png)

- In the Configure Docker Repository page, you must select one of the Docker repository options. Use an embedded Docker Repository - Copies all images (Internet or AirGapped) to the embedded registry. If you select Use an embedded Docker Repository option, then you can download and deploy the Data Services that you need for your cluster.
    - By selecting Default, all the data services will be downloaded and deployed.
    - By selecting Select the optional images:
        - If you switch off the Machine Learning toggle key, then the Machine Learning runtimes will not be installed.
        - If you switch on the Machine Learning toggle key, then the Machine Learning runtimes will be installed.
    - Click Continue.

![](../../assets/images/ds/freshinstall08.png)

- In the Configure Data Services page, set the following parameters, appropriate for your env:
```
Example:
Docker directory: /docker
Data Storage Directory: /mnt2/ecs/longhorn-storage
Local Path Storage Directory: /mnt/ecs/local-storage
Application Domain: ecs-lb.sme-feng.athens.cloudera.com
```
**_NOTE:_** Application Domain maps to the  pre-defined wildcard DNS record which allows the resolution of `*.apps.ecs133.train.athens.cloudera.com` to the IP address of the HAProxy host. MUST be done before you proceed. You can verify from command line using nslookup or dig

- Click Continue.

![](../../assets/images/ds/freshinstall09.png)

- In the Configure Databases page, follow the instructions in the wizard to use your external existing databases with CDP Private Cloud.
Click Continue.

**_NOTE:_** Ensure that you have selected the Use TLS for Connections Between the Control Plane and the Database option if you have plans to use Cloudera Data Warehouse (CDW). Enabling the Private Cloud Base Cluster PostgreSQL database to use an SSL connection to encrypt client-server communication is a requirement for CDW in CDP Private Cloud.

![](../../assets/images/ds/freshinstall10.png)

![](../../assets/images/ds/freshinstall11.png)

- In the Install Parcels page, the selected parcels are downloaded and installed on the host cluster. Click Continue.

![](../../assets/images/ds/freshinstall12.png)

- In the Inspect Cluster page, you can inspect your network performance and hosts. If the inspect tool displays any issues, you can fix those issues and run the inspect tool again. Click Continue.

![](../../assets/images/ds/freshinstall13.png)

- In the Install Data Services page, you will see the installation process.

![](../../assets/images/ds/freshinstall14.png)

- After the installation is complete, you will see the Summary image. You can Launch CDP Private Cloud.

![](../../assets/images/ds/freshinstall15.png)

- After the installation is complete, you can access your Private Cloud Data Services instance from Cloudera Manager > click Open Private Cloud Data Services.

![](../../assets/images/ds/freshinstall16.png)

- Confirm that all backends of HAProxy are now status UP, it may take several minutes.

![](../../assets/images/ds/freshinstall17.png)

- Confirm that all pods are green in the ECS WebUI >> (All Namespaces) >> Workloads.

![](../../assets/images/ds/freshinstall18.png)

