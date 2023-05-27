---
layout: default
title: CDSW > CML Migration
nav_order: 7
parent: Operations
grand_parent: Data Service
---

# CDSW > CML Migration
{: .no_toc }

- TOC
{:toc}

---

- The CDSW service is deployed on the client nodes of the CDP Base cluster, while the CML is deployed on the ECS cluster which is attached to the CDP Base cluster. Therefore, the migration of CDSW to CML is not equivalent. A seperate ECS cluster must be built at first and the size of ECS cluster may exceed CDSW nodes.
    - For example: 1 CDSW master + 1 CDSW worker requires at least 3 ECS nodes (For ECS Master HA). The following demonstration is the migration steps from 2 CDSW nodes to 3 ECS master nodes.

![](../../assets/images/ds/cdswmig01.png)

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7 SP2|
|CM version |Cloudera Manager 7.9.5|
|ECS version |CDP PvC DataServices 1.5.0|
|OS version |Centos 7.9|
|K8S version |RKE 1.21|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |Yes|
|Kerberos |FreeIPA|
|LDAP |FreeIPA|
|DB Configuration |PostgreSQL 10.21|
|Vault |Embedded|
|Docker registry |Embedded|
|Install Method |Internet|
|CDSW version|1.10.3|


## 2. CDSW Migration

### 2.1 Repurpose CDP Base nodes for ECS Cluster

- 1 CDSW master + 1 CDSW worker needs to be setup side-by-side with CDSW to migrate the projects. 3 nodes of the ECS cluster need to be fetched from the CDP Base Cluster. Please see [Repurposing CDP Private Cloud Base Nodes for CDP Private Cloud Data Services on ECS](https://docs.cloudera.com/cdp-private-cloud-data-services/1.5.0/repurposing-nodes/topics/cdppvc-data-services-repurposing-nodes.html).

### 2.2 Install ECS Cluster

- The ECS node in the production environment requires at least 3 master nodes, and no worker nodes are required, because the master nodes can also serve as worker nodes. Please see [Installing ECS HA cluster](https://fxu1024.github.io/docs/ds/freshinstall/)

- Note: In order to use the ECS worker as the ECS master, you have to manually cleanup the taint after installation.
```bash
kubectl taint nodes <Master01s hostname> node-role.kubernetes.io/control-plane=true:NoSchedule-
kubectl taint nodes <Master02s hostname> node-role.kubernetes.io/control-plane=true:NoSchedule-
kubectl taint nodes <Master03s hostname> node-role.kubernetes.io/control-plane=true:NoSchedule-
```


### 2.3 Use the CDSW to CML migration tool

- Log into CDP Private Cloud 1.5.0, and navigate to Cloudera Machine Learning > Workspaces. The system detects the presence of your legacy CDSW installation. Click Upgrade.

![](../../assets/images/ds/cdswmig02.png)

- Click File Upload > Choose File, go to /etc/kubernetes/admin.conf on the CDSW cluster host, and select the Kubeconfig file.
    - In Migration timeout, accept the default 1440 minutes (24 hours) timeout, or if your CDSW workload is hundreds of gigabytes, increase the migration time up to 2880 minutes (2 days). Increasing the migration timeout value does not cause a delay in the migration of a small workload.

![](../../assets/images/ds/cdswmig03.png)

- In Workspace Name, type an arbitrary name. In Select Environment, select your CDP environment. Accept default values for other options, and click Provision Workspace.

![](../../assets/images/ds/cdswmig04.png)

- Execute the following script to create external nfs for CML

```bash
echo "/dev/vdb    /mnt/vfs   xfs defaults    0   0" >> /etc/fstab
mkdir -p /mnt/vfs
echo "/mnt/vfs *(rw,sync,no_root_squash,no_all_squash,no_subtree_check)" > /etc/exports
exportfs -rv
showmount -e

mkdir /mnt/vfs/workspace1
chown 8536:8536 /mnt/vfs/workspace1
chmod g+srwx /mnt/vfs/workspace1

yum install nfs-utils.x86_64 -y
systemctl start nfs-server.service
systemctl enable nfs-server.service
mkdir -p /mnt/nfs
mount -t nfs -o vers=4.1 feng-ws5.sme-feng.athens.cloudera.com:/mnt/vfs/workspace1 /mnt/nfs
nfsstat -m|grep /mnt/nfs
```

![](../../assets/images/ds/cdswmig05.png)

- Accept default values for other options, and click Provision Workspace

- CML installation begins, and the CDSW to CML migration follows automatically. Status indicators show the progress of the installation and migration. During the migration, you cannot access the CDSW cluster. The migration process stops CDSW pods to prevent data corruption. After migration, the CDSW returns to a working state. The CML workspace is stopped.

![](../../assets/images/ds/cdswmig06.png)



