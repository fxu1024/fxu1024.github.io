---
layout: default
title: Issues
nav_order: 3
has_children: true
parent: Data Service
---

# DS Issues
{: .no_toc }

- TOC
{:toc}

---

## 1. rendered manifests contain a resource that already exists

--- 
PROBLEM: 
{: .label .label-yellow } 

- failed to activate CDE service

```console
2021-09-07T01:40:29.556957Z:LogDebug:Error fetching chart info for dex-base, invalid chart, will retry
Sep 7, 2021, 9:40:30 AM:LogError:dex-base, version 1.10.0 installation failed, dex-base installation failed, rendered manifests contain a resource that already exists. Unable to continue with install: existing resource conflict: namespace: , name: pvccde-dex-base-dex-base-configs-manager, existing_kind: rbac.authorization.k8s.io/v1, Kind=ClusterRole, new_kind: rbac.authorization.k8s.io/v1, Kind=ClusterRole
```
--- 
CAUSE: 
{: .label .label-red }

- Deleting from the CDE UI does not delete records in the backend database. 

---  
RESOLUTION: 
{: .label .label-green } 
   
```bash
kubectl exec -it cdp-embedded-db-0 -n cp -- bash
psql -P pager=off -d db-dex

delete from instance where clusterid = 'cluster-spzq7cvg';

delete from cluster where id = 'cluster-spzq7cvg';
```

## 2. Name or service not known

--- 
PROBLEM: 
{: .label .label-yellow } 

- Get errors when installing Control Plane :
Process install-cp (id=1546338729) on host ip-10-113-204-13.se.fuse.cloudera.com (id=1546338574) exited with 1 and expected 0

```console
+ ./install-cdp.sh -n cp
+ popd
+ pushd logs
+ python /opt/cloudera/cm-agent/service/ecs/get_creds.py https://console-cp.apps.ecs-ycloud.ecs.openstack.com
Traceback (most recent call last):
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 64, in <module>
    result = generate_initial_access_and_private_keys(sys.argv[1])
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 15, in generate_initial_access_and_private_keys
    local_account_id = get_cdp_account_id(management_console_url)
  File "/opt/cloudera/cm-agent/service/ecs/get_creds.py", line 49, in get_cdp_account_id
    initial_auth_response = requests.get(api_path, verify=False)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 68, in get
    return request('get', url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/api.py", line 50, in request
    response = session.request(method=method, url=url, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 486, in request
    resp = self.send(prep, **send_kwargs)
  File "/usr/lib/python2.7/site-packages/requests/sessions.py", line 598, in send
    r = adapter.send(request, **kwargs)
  File "/usr/lib/python2.7/site-packages/requests/adapters.py", line 415, in send
    raise ConnectionError(err, request=request)
requests.exceptions.ConnectionError: ('Connection aborted.', gaierror(-2, 'Name or service not known'))
```
--- 
CAUSE: 
{: .label .label-red }

- need to define wildcard DNS entry `*.apps.ecs-ycloud.ecs.openstack.com`. The app domain describes a dns subdomain set up for ecs/ocp, within that dns subdomain we expect to have an A-Record with wildcard resolving to IP address of the ECS Server (or to the VIP of a Loadbalancer, when using ECSMaster HA).

---  
RESOLUTION: 
{: .label .label-green } 

The sample example for AD using DNS Manager:

![](../../assets/images/ds/adddns03.png)

The sample example for FreeIPA using DNS Zones:

![](../../assets/images/ds/ipadns04.jpg)

The sample example for dnsmasq using `address`:

```bash
echo "strict-order
user=root
listen-address=172.27.27.9
address=/apps.ecs-ycloud.ecs.openstack.com/192.168.8.144
addn-hosts=/etc/dnsmasq.hosts
resolv-file=/etc/resolv.dnsmasq.conf
conf-dir=/etc/dnsmasq.d" > /etc/dnsmasq.conf

systemctl restart dnsmasq
```


## 3. Non supported character set (add orai18n.jar in your classpath): ZHS16GBK

--- 
PROBLEM: 
{: .label .label-yellow } 

- Get errors from cloudera-scm-service.log

```console
2022-08-01 20:03:28,371 ERROR main:com.cloudera.server.cmf.bootstrap.EntityManagerFactoryBean: Unable to access schema version in database.
javax.persistence.PersistenceException: org.hibernate.exception.GenericJDBCException: could not execute query

Caused by: org.hibernate.exception.GenericJDBCException: could not execute query

Caused by: java.sql.SQLException: Non supported character set (add orai18n.jar in your classpath): ZHS16GBK
```

- Get errors from hadoop-cmf-hive-HIVEMETASTORE-<HOSTNAME>.log

```console
[pool-6-thread-67]: Internal error processing lock
org.apache.hadoop.hive.metastore.api.MetaException: Unable to update transaction database java.sql.SQLException: Non supported character set (add orai18n.jar in your classpath): ZHS16GBK
```

- Get errors from container metastore in pod metastore-0

```console
level="ERROR" thread="pool-12-thread-71"] MetaException(message:Unable to update transaction database java.sql.SQLException: Non supported character set (add orai18n.jar in your classpath): ZHS16GBK\r	at oracle.sql.CharacterSetUnknown.failCharsetUnknown(CharacterSetFactoryThin.java:233)
```

--- 
ENVIRONMENT: 
{: .label .label-yellow }

- ECS - 1.4.0
- Oracle DB backend

--- 
CAUSE: 
{: .label .label-red }

- Ensure that ojdbc8.jar and orai18n.jar are present in the Hive CLASSPATH, for using Oracle as backend DB.
    - ojdbc8.jar is JDBC driver used by Spark or Hadoop tasks to connect to the database.
    - orai18n.jar offers Oracle Globalization Support.

---  
RESOLUTION: 
{: .label .label-green } 

- For Cloudera Manager Server:

```bash
systemctl stop cloudera-scm-server

vi /etc/default/cloudera-scm-server

- export CMF_JDBC_DRIVER_JAR="/usr/share/java/mysql-connector-java.jar:/usr/share/java/oracle-connector-java.jar:/usr/share/java/postgresql-connector-java.jar"  
+ export CMF_JDBC_DRIVER_JAR="/usr/share/java/mysql-connector-java.jar:/usr/share/java/oracle-connector-java.jar:/usr/share/java/postgresql-connector-java.jar:/usr/share/oracle/instantclient/orai18n.jar"  

systemctl start cloudera-scm-server
```

- For Hive metastore in CDP Base:

```bash
cp /usr/share/oracle/instantclient/orai18n.jar /opt/cloudera/parcels/CDH/lib/hive/lib
```
and then restart HMS. 

- For Hive metastore in CDW Private Cloud:

```bash
kubectl scale -n warehouse-1659681455-fh9p sts metastore --replicas=0
kubectl -n warehouse-1659681455-fh9p edit sts metastore

          command:
            - sh
            - '-c'
            - wget http://cb04.ecs.ycloud.com/oracle/orai18n.jar -O /aux-jars/orai18n.jar;/aux-jars-localizer.sh

kubectl scale -n warehouse-1659681455-fh9p sts metastore --replicas=2
```
This a tricky way to upload orai18n.jar into /aux-jars in container metastore by wget commandline.

## 4. ORA-02289: sequence does not exist

--- 
PROBLEM: 
{: .label .label-yellow } 

- Get errors from /var/log/cloudera-scm-headlamp/mgmt-cmf-mgmt-REPORTSMANAGER-cb01.ecs.ycloud.com.log.out

```console
Encountered exception
javax.persistence.PersistenceException: org.hibernate.exception.SQLGrammarException: could not extract ResultSet
	at org.hibernate.internal.ExceptionConverterImpl.convert(ExceptionConverterImpl.java:154)
	at org.hibernate.internal.ExceptionConverterImpl.convert(ExceptionConverterImpl.java:181)
	at org.hibernate.internal.ExceptionConverterImpl.convert(ExceptionConverterImpl.java:188)
	at org.hibernate.internal.SessionImpl.firePersist(SessionImpl.java:726)
	at org.hibernate.internal.SessionImpl.persist(SessionImpl.java:706)
	at com.cloudera.headlamp.BeancounterDiskUsagePersistenceThread.persistUserGroupSummaries(BeancounterDiskUsagePersistenceThread.java:170)
	at com.cloudera.headlamp.BeancounterDiskUsagePersistenceThread.work(BeancounterDiskUsagePersistenceThread.java:89)
	at com.cloudera.headlamp.BeancounterDiskUsagePersistenceThread.run(BeancounterDiskUsagePersistenceThread.java:51)
Caused by: org.hibernate.exception.SQLGrammarException: could not extract ResultSet
Caused by: Error : 2289, Position : 7, Sql = select RMAN_USERGROUPHISTORY_SEQ.nextval from dual, OriginalSql = select RMAN_USERGROUPHISTORY_SEQ.nextval from dual, Error Msg = ORA-02289: sequence does not exist

	at oracle.jdbc.driver.T4CTTIoer11.processError(T4CTTIoer11.java:513)
	... 28 more
```

--- 
ENVIRONMENT: 
{: .label .label-yellow }

- ECS - 1.4.0
- Oracle DB backend

--- 
CAUSE: 
{: .label .label-red }

- There was no changes regarding the sequence creation of this database for a long time. It's possible that there will be other corrupted part of the database.

---  
RESOLUTION: 
{: .label .label-green } 

- To recreate the missing sequence in that way:
    - select max(id) from RMAN.RMAN_USERGROUPHISTORY;
    - CREATE SEQUENCE rman.RMAN_USERGROUPHISTORY_SEQ start with <something bigger than the max(id)>; 
   
```console
SQL> select max(id) from RMAN.RMAN_USERGROUPHISTORY;

   MAX(ID)
----------
      4947

SQL> CREATE SEQUENCE RMAN.RMAN_USERGROUPHISTORY_SEQ start with 5000;

Sequence created.
```


## 5. issue template

--- 
PROBLEM: 
{: .label .label-yellow } 

- 

```console
```

--- 
ENVIRONMENT: 
{: .label .label-yellow }

- ECS - All Versions 

--- 
CAUSE: 
{: .label .label-red }

- 

---  
RESOLUTION: 
{: .label .label-green } 
   
```bash
```


## n. issue template

--- 
PROBLEM: 
{: .label .label-yellow } 

- 

```console
```

--- 
ENVIRONMENT: 
{: .label .label-yellow }

- ECS - All Versions 

--- 
CAUSE: 
{: .label .label-red }

- 

---  
RESOLUTION: 
{: .label .label-green } 
   
```bash
```

