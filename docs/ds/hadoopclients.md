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

- Connect to CDW VW using LDAP authentication.
    - beeline command `beeline -u 'jdbc:hive2://hs2-hive01.apps.ecs-lb.sme-feng.athens.cloudera.com/default;transportMode=http;httpPath=cliservice;ssl=false;retries=3' -n admin -p`

![](../../assets/images/ds/gateway004.jpg)

This shows that Standalone Beeline CLI supports LDAP authentication.

- Connect to CDP Base cluster using Kerberos authentication.
    - beeline commands `beeline -u 'jdbc:hive2://ccycloud-1.tiger.root.hwx.site:10000/default;principal=hive/_HOST@FENG.COM;ssl=true;sslTrustStore=cm-auto-in_cluster_truststore.jks'`

![](../../assets/images/ds/gateway003.jpg)

This shows that Standalone Beeline CLI supports Kerberos authentication.





