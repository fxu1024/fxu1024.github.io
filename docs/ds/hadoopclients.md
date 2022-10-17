---
layout: default
title: Setting up Hadoop Client on MacOS
nav_order: 4
parent: Operations
grand_parent: Data Service
---

# Setting up Hadoop Client on MacOS
{: .no_toc }

- TOC
{:toc}

---

This topic would allow you to access HDFS, submit yarn/spark jobs, connect to hive using beeline from your MAC computer.

## 1. Standalone Beeline

- In order to connect to Hive VW via beeline shell, the first step is to download Beeline CLI software. Click on the 3 dots beside the HUE button, and click on the ["Download Beeline CLI"](https://cdw-ui.s3.amazonaws.com/hive3/beeline-standalone/apache-hive-beeline-3.1.3000.tar.gz).

![](../../assets/images/ds/gateway001.jpg)

- Extract the tar.gz file, and you will see two folders, bin & lib
```bash
mkdir -p ~/hadoop-clients
tar xvzf apache-hive-beeline-3.1.3000.tar.gz -C ~/hadoop-clients
cd ~/hadoop-clients
mv apache-hive-beeline-3.1.3000.2022.0.8.0-3 cdw-beeline
```
![](../../assets/images/ds/gateway002.jpg)

- Beeline requires Java to be available, so install JDK as well.
```console
$ java -version
java version "1.8.0_341"
Java(TM) SE Runtime Environment (build 1.8.0_341-b10)
Java HotSpot(TM) 64-Bit Server VM (build 25.341-b10, mixed mode)
```

- Beelne requires config files from CDP Base cluster(/etc/hive/conf.cloudera.hive_on_tez)
```bash
# gen tarball on CDP Base node
tar cvf hiveconf.tar /etc/hive/conf.cloudera.hive_on_tez
```

```bash
# extrace tarball on MAC laptop
tar xvf hiveconf.tar -C ~/hadoop-clients/cdw-beeline
```

- Modify `.bash_profile`
```bash
echo "export PATH=/Users/feng.xu/hadoop-clients/cdw-beeline/bin:$PATH
export HADOOP_CONF_DIR=/Users/feng.xu/hadoop-clients/cdw-beeline/etc/hive/conf.cloudera.hive_on_tez
export JAVA_HOME=/Library/Internet\ Plug-Ins/JavaAppletPlugin.plugin/Contents/Home" >> ~/.bash_profile
source ~/.bash_profile
```

- Connect to Hive in CDP Base cluster using Kerberos authentication.

```bash
beeline -u 'jdbc:hive2://ccycloud-1.tiger.root.hwx.site:10000/default;principal=hive/_HOST@FENG.COM;ssl=true;sslTrustStore=cm-auto-in_cluster_truststore.jks'
```

![](../../assets/images/ds/gateway003.jpg)

- Connect to Impala in CDP Base cluster using LDAP authentication.

```bash
export HIVE_AUX_JARS_PATH=/Users/feng.xu/projects/ImpalaJDBC41.jar
beeline -d 'com.cloudera.impala.jdbc41.Driver' -u 'jdbc:impala://ccycloud-3.tiger.root.hwx.site:21050;AuthMech=3;uid=admin;pwd=xxx;SSL=1;sslTrustStore=/Users/feng.xu/hadoop-clients/cm-auto-in_cluster_truststore.jks'
```

![](../../assets/images/ds/gateway005.jpg)

- Connect to Hive VW in PvC CDW using LDAP authentication.

```bash
beeline -u 'jdbc:hive2://hs2-hive01.apps.ecs-lb.sme-feng.athens.cloudera.com/default;transportMode=http;httpPath=cliservice;ssl=false;retries=3' -n admin -p
```

![](../../assets/images/ds/gateway004.jpg)

- Connect to Impala VW in PvC CDW using LDAP authentication.

```bash
export host=coordinator-impala01.apps.ecs-lb.sme-feng.athens.cloudera.com
export file=pvc140_impala
rm -f $file.jks $file.pem
openssl s_client -showcerts -connect $host:443 -servername $host </dev/null 2>/dev/null|openssl x509 -outform PEM > $file.pem
keytool -import -alias $host -file $file.pem -keystore $file.jks
export HIVE_AUX_JARS_PATH=/Users/feng.xu/projects/ImpalaJDBC41.jar
beeline -d "com.cloudera.impala.jdbc41.Driver" -u "jdbc:impala://coordinator-impala01.apps.ecs-lb.sme-feng.athens.cloudera.com:443/default;AuthMech=3;transportMode=http;httpPath=cliservice;ssl=1;sslTrustStore=/Users/feng.xu/pvc140_impala.jks;trustStorePassword=123456"
```

![](../../assets/images/ds/gateway006.jpg)

It returned error messages "Error setting/closing session: HTTP Response code: 401". This shows that beeline does not support direct access to impala VW.

