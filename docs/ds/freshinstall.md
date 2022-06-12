---
layout: default
title: fresh install of ECS 1.3.4 HA
nav_order: 3
parent: Operations
grand_parent: Data Service
---

# Add new worker node to the existing ECS cluster
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

## 2. install ECS HA cluster

- In Cloudera Manager, on the top right corner, click Add > Add Cluster. In the Select Cluster Type page, select the cluster type as Private Cloud Containerized Cluster and click Continue.

![](../../assets/images/ds/freshinstall00.png)

- On the Getting Started page of the installation wizard, select Internet Install Method. To use a custom repository link provided to you by Cloudera, click Custom Repository. Click Continue.

![](../../assets/images/ds/freshinstall01.png)

- In the Cluster Basics page, type a name for the Private Cloud cluster that you want to create in the Cluster Name field. From the Base Cluster drop-down list, select the cluster that has the storage and SDX services that you want this new Private Cloud Data Services instance to connect with. Click Continue.

![](../../assets/images/ds/freshinstall02.png)

- In the Specify Hosts page, provide a list of available hosts or you can add new hosts. You can provide the Fully Qualified Domain Name (FQDN) in the following patterns:
You can specify multiple addresses and address ranges by separating them by commas, semicolons, tabs, or blank spaces, or by placing them on separate lines. Use this technique to make more specific searches instead of searching overly wide ranges.

![](../../assets/images/ds/freshinstall03.png)

- In the Assign Roles page, you can customize the roles assignment for your new Private Cloud Containerized cluster. Click Continue.

![](../../assets/images/ds/freshinstall04.png)

![](../../assets/images/ds/freshinstall05.png)

![](../../assets/images/ds/freshinstall06.png)

![](../../assets/images/ds/freshinstall07.png)

- In the Configure Docker Repository page, you must select one of the Docker repository options. Use an embedded Docker Repository - Copies all images (Internet or AirGapped) to the embedded registry. If you select Use an embedded Docker Repository option, then you can download and deploy the Data Services that you need for your cluster.
By selecting Default, all the data services will be downloaded and deployed.
By selecting Select the optional images:
If you switch off the Machine Learning toggle key, then the Machine Learning runtimes will not be installed.
If you switch on the Machine Learning toggle key, then the Machine Learning runtimes will be installed.
Click Continue.

![](../../assets/images/ds/freshinstall08.png)

- In the Configure Data Services page, you can modify configuration settings such as the data storage directory, number of replicas, and so on. If there are multiple disks mounted on each host with different characteristics (HDD and SSD), then Local Path Storage Directory must point to the path belonging to the optimal storage. Ensure that you have reviewed your changes. If you want to specify a custom certificate, place the certificate and the private key in a specific location on the Cloudera Manager server host and specify the paths in the input boxes labelled as Ingress Controller TLS/SSL Server Certificate/Private Key File below. This certificate will be copied to the Control Plane during the installation process.
Click Continue.

![](../../assets/images/ds/freshinstall09.png)

- In the Configure Databases page, follow the instructions in the wizard to use your external existing databases with CDP Private Cloud.
Click Continue.
Ensure that you have selected the Use TLS for Connections Between the Control Plane and the Database option if you have plans to use Cloudera Data Warehouse (CDW). Enabling the Private Cloud Base Cluster PostgreSQL database to use an SSL connection to encrypt client-server communication is a requirement for CDW in CDP Private Cloud.

![](../../assets/images/ds/freshinstall10.png)

![](../../assets/images/ds/freshinstall11.png)

- In the Install Parcels page, the selected parcels are downloaded and installed on the host cluster. Click Continue.

![](../../assets/images/ds/freshinstall12.png)

- In the Inspect Cluster page, you can inspect your network performance and hosts. If the inspect tool displays any issues, you can fix those issues and run the inspect tool again.
Click Continue.

![](../../assets/images/ds/freshinstall13.png)

- In the Install Data Services page, you will see the installation process.

![](../../assets/images/ds/freshinstall14.png)

- After the installation is complete, you will see the Summary image. You can Launch CDP Private Cloud.

![](../../assets/images/ds/freshinstall15.png)

After the installation is complete, you can access your Private Cloud Data Services instance from Cloudera Manager > click Open Private Cloud Data Services.

![](../../assets/images/ds/freshinstall16.png)

