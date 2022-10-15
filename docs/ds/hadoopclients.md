---
layout: default
title: Custom Standalone Gateway Node 
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

## 1. Standalone Beeline for CDW

- In order to connect to Hive VW via beeline shell, the first step is to download Beeline CLI software. Click on the 3 dots beside the HUE button, and click on the [Download Beeline CLI](https://cdw-ui.s3.amazonaws.com/hive3/beeline-standalone/apache-hive-beeline-3.1.3000.tar.gz).

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
java version "1.8.0_144"
Java(TM) SE Runtime Environment (build 1.8.0_144-b01)
Java HotSpot(TM) 64-Bit Server VM (build 25.144-b01, mixed mode)
```

- Modify `.bash_profile`
```bash
echo "export PATH=/Users/feng.xu/hadoop-clients/cdw-beeline/bin:$PATH
export JAVA_HOME=/Library/Java/JavaVirtualMachines/jdk1.8.0_144.jdk//Contents/Home" >> ~/.bash_profile
source ~/.bash_profile
```

- Connect to CDP Base cluster using Kerberos authentication.
    - beeline commands `beeline -u 'jdbc:hive2://ccycloud-1.tiger.root.hwx.site:10000/default;principal=hive/ccycloud-1.tiger.root.hwx.site@FENG.COM;ssl=true;sslTrustStore=cm-auto-in_cluster_truststore.jks`

![](../../assets/images/ds/gateway003.jpg)

It failed with the following error: `WARN util.NativeCodeLoader: Unable to load native-hadoop library for your platform... using builtin-java classes where applicable`.

- Connect to CDW VW using LDAP authentication.
    - beeline command `beeline -u 'jdbc:hive2://hs2-hive01.apps.ecs-lb.sme-feng.athens.cloudera.com/default;transportMode=http;httpPath=cliservice;ssl=false;retries=3' -n admin -p`

![](../../assets/images/ds/gateway004.jpg)

This shows that the current Beeline CLI provided by CDW only supports LDAP authentication.

## 2. Standalone Beeline for CDP Base cluster




