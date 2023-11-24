---
layout: default
title: CML Quota Management Testing
nav_order: 18
parent: Operations
grand_parent: Data Service
---

# CML Quota Management Testing
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

- Quota management enables you to control how resources are allocated within your CML workspace.
    - `Object Quota`: Each user can only run 50 Pods in parallel (sessions, jobs, Spark drivers+executors, etc). You can set the OVERRIDE_PODQUOTA environment variable in the project to override the default value.
    - `User Level Quota`: CML administrators can enable user level quota under Site Administration Page. By default, 8 GiB memory and 2 vCPU cores are configured for each user. The custom quota can override the default quota for the dedicated user.
    - `Namespace Level Quota`(new feature starting from 1.5.2): Resource Pools are organized in a hierarchical manner by defining nodes in the hierarchy with resource limits, which can then be subdivided as needed to allocate resources for a new namespace. CML has two types of namespace: Infra namespace and User namespace. 1 CML workspace has one infra namespace and many user namespaces. Use namespace is created dynamically when any workload is run (like session, job etc) based on infra namespace name with suffixes of -user-<userid>. This means that each user has its own working namespace.



