---
layout: default
title: CDW Quota Management Testing
nav_order: 17
parent: Operations
grand_parent: Data Service
---

# CDW Quota Management Testing
{: .no_toc }

- TOC
{:toc}

---

## 1. Introduction to the test environment

|CDP Runtime version |CDP PvC Base 7.1.7 SP2|
|CM version |Cloudera Manager 7.11.3.2|
|ECS version |CDP PvC DataServices 1.5.2|
|OS version |Centos 7.9|
|K8S version |RKE 1.25.14|
|Whether to enable Kerberos |Yes|
|Whether to enable TLS |Yes|
|Auto-TLS |Yes|
|Kerberos |FreeIPA|
|LDAP |FreeIPA|
|DB Configuration |Embedded|
|Vault |Embedded|
|Docker registry |Embedded|
|Install Method |Internet|

## 2. Basic Concept

- By enabling quota management in Cloudera Data Warehouse (CDW) on Private Cloud, you can assign quota-managed resource pools for environments, Data Catalogs, Virtual Warehouses, and Data Visualization instances.

## 3. Add new pool for Data Services 

- RPM (Resouce Pool Manager) is tracking resources across K8s clusters through resource pool objects. Resouce pool objects allow for defining a hierarchical structure for purposes of ownership and quota management.

- Navigate to Cloudera Management Console > Resource Utilization > Quotas, and add three new pools for Data Services workloads. 
    - Note: please keep advanced properties no changed. 

|No.|PATH|quota_cores|quota_memory|validity|distribution|order|queueing|clusterId|namespace|
|1|root.default.high|48|200GB||ELASTIC|FIFO|true|||
|2|root.default.medium|24|100GB||ELASTIC|FIFO|true|||
|3|root.default.low|12|50GB||ELASTIC|FIFO|true|||

![](../../assets/images/ds/cdwquota03.png)

![](../../assets/images/ds/cdwquota04.png)

![](../../assets/images/ds/cdwquota05.png)


## 4. Enable quota management for CDW

- Log in to CDW as user `admin`. Go to Advanced Configuration and select the Enable quota management option. Click Update.
    - Note: You must enable this feature before activating an environment in CDW. You cannot enable this feature in existing environments; you will need to deactivate the environment in CDW, enable the quota management feature, and then reactivate the environment.

![](../../assets/images/ds/cdwquota01.png)

- Activate the environment.

![](../../assets/images/ds/cdwquota06.png)

- Select the resource pool `root.default.high`.
    - Note: If you enable the quota management feature, you must select a resource pool while activating the environment.

![](../../assets/images/ds/cdwquota07.png)

- Turn back to the resource pool UI. the resource pool `root.default.high` has two new level 4 branches, namely `root.default.high.ecstest-c51569f2-log-router` and `root.default.high.warehouse-ecstest`.

![](../../assets/images/ds/cdwquota13.png)

- `ecstest-c51569f2-log-router` and `warehouse-ecstest` are the new namespaces added by the activation environment step.
    - The pool `root.default.high.ecstest-c51569f2-log-router` consumed 4 cores, 2GB memory.
    - The pool `root.default.high.warehouse-ecstest`consumed 6 cores, 16GB memory.
    - Total cpu and memory consumption is below quota, so there are no warnings so far.

![](../../assets/images/ds/cdwquota14.png)
 
- Create new virtual warehouse `hive01`.

![](../../assets/images/ds/cdwquota08.png)

- The resource pool has only one option `root.default.high`, indicating that it is inherited from environment.

![](../../assets/images/ds/cdwquota09.png)

- Turn back to the resource pool UI. We can see the new resource pool `root.default.high.compute-hive01`.

![](../../assets/images/ds/cdwquota15.png)

- `compute-hive01`is the namespace of hive virtual warehouse.
    - The pool `root.default.high.compute-hive01` consumed 12 cores, 128GB memory.

![](../../assets/images/ds/cdwquota16.png)

![](../../assets/images/ds/cdwquota10.png)


## 5. Technical Preview in 1.5.2

- CDW Quota Management is technical preview in 1.5.2 which's generally not ready for production deployment. You should explore this feature in a non production cluster.

- Only 4 pods in hive virtual warehouse use yunikorn scheduler.
    - The default k8s scheduler take over when `yunikorn.apache.org/ignore-application` is `true`.

```bash
$ for pod in $(kubectl get pod -n compute-hive01 --output=jsonpath={.items..metadata.name}); do echo $pod && kubectl describe pod $pod -n compute-hive01|grep yunikorn.apache.org; done
hiveserver2-0
              yunikorn.apache.org/ignore-application: true
hue-huedb-create-job-ggpkn
              yunikorn.apache.org/ignore-application: true
huebackend-0
              yunikorn.apache.org/ignore-application: true
huefrontend-65b995bdcc-zzrgf
              yunikorn.apache.org/ignore-application: true
query-coordinator-0-0
              yunikorn.apache.org/allow-preemption: true
              yunikorn.apache.org/scheduled-at: 1700796724189880458
query-coordinator-0-1
              yunikorn.apache.org/allow-preemption: true
              yunikorn.apache.org/scheduled-at: 1700796724222578763
query-executor-0-0
              yunikorn.apache.org/allow-preemption: true
              yunikorn.apache.org/scheduled-at: 1700796724282562442
query-executor-0-1
              yunikorn.apache.org/allow-preemption: true
              yunikorn.apache.org/scheduled-at: 1700796724254507099
standalone-compute-operator-0
              yunikorn.apache.org/ignore-application: true
usage-monitor-57d5977ccb-plrjt
              yunikorn.apache.org/ignore-application: true
```

- All pods in impala virtual warehouse use the default k8s scheduler.
    - The default k8s scheduler take over when `yunikorn.apache.org/ignore-application` is `true`.

```bash
$ for pod in $(kubectl get pod -n impala-impala01 --output=jsonpath={.items..metadata.name}); do echo $pod && kubectl describe pod $pod -n impala-impala01|grep yunikorn.apache.org; done
catalogd-0
              yunikorn.apache.org/ignore-application: true
catalogd-1
              yunikorn.apache.org/ignore-application: true
coordinator-0
              yunikorn.apache.org/ignore-application: true
coordinator-1
              yunikorn.apache.org/ignore-application: true
hue-huedb-create-job-xq6mz
              yunikorn.apache.org/ignore-application: true
huebackend-0
              yunikorn.apache.org/ignore-application: true
huefrontend-7d46c4465-8gtrx
              yunikorn.apache.org/ignore-application: true
impala-autoscaler-5655fb65c-tc6qz
              yunikorn.apache.org/ignore-application: true
impala-executor-000-0
              yunikorn.apache.org/ignore-application: true
impala-executor-000-1
              yunikorn.apache.org/ignore-application: true
statestored-f96f8bc6-85hx4
              yunikorn.apache.org/ignore-application: true
```

- All pods in `warehouse` and `log-router` namespace use the default k8s scheduler as well.

## 6. Conclusion

- CDW Quota Management is Technical Preview in PvC 1.5.2. However, most pods still use the default k8s scheduler, so it is currently not recommended for a production cluster.
